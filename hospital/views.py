from django.shortcuts import render
from rest_framework import generics, status, permissions
from datetime import datetime, timedelta

# Home page is now handled by Next.js frontend - view removed
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import (
    RegisterSerializer, UserSerializer, 
    PatientProfileSerializer, DoctorProfileSerializer, 
    NurseProfileSerializer, StaffProfileSerializer,
    AppointmentSerializer, AppointmentCreateSerializer,
    AppointmentUpdateSerializer, DoctorListSerializer,
    AvailableSlotSerializer,
    MedicalRecordSerializer, MedicalRecordCreateSerializer,
    MedicalRecordUpdateSerializer, PatientMedicalHistorySerializer
)
from .models import Patient, Doctor, Nurse, Staff, Appointment, MedicalRecord
from .permissions import (
    IsAdmin, IsDoctor, IsPatient, 
    IsPatientOrAdmin, IsAppointmentOwnerOrDoctor, CanCancelAppointment
)
from django.utils import timezone

User = get_user_model()

class RegisterPatientView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save(role='PATIENT')
        # Create empty patient profile
        # Patient.objects.create(user=user, age=0, gender='O', contact_info='') 
        # Note: We might want to require profile data at registration or let them update it later.
        # For now, let's just create the user. Profile creation can be a separate step or included here if we expand the serializer.

class RegisterStaffView(generics.CreateAPIView):
    """
    Only Admins can register staff (Doctors, Nurses, Receptionists).
    """
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)
    serializer_class = RegisterSerializer

class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        data = serializer.data
        
        # Add profile data based on role
        if user.role == 'PATIENT':
            try:
                profile = user.patient_profile
                data['profile'] = PatientProfileSerializer(profile).data
            except Patient.DoesNotExist:
                data['profile'] = None
        elif user.role == 'DOCTOR':
            try:
                profile = user.doctor_profile
                data['profile'] = DoctorProfileSerializer(profile).data
            except Doctor.DoesNotExist:
                data['profile'] = None
        # ... Add other roles as needed
        
        return Response(data)

    def post(self, request):
        user = request.user
        data = request.data
        
        if user.role == 'PATIENT':
            # Get or create patient profile with defaults for required fields
            profile, created = Patient.objects.get_or_create(
                user=user,
                defaults={
                    'age': data.get('age', 0),
                    'gender': data.get('gender', 'O'),
                    'contact_info': data.get('contact_info', '')
                }
            )
            serializer = PatientProfileSerializer(profile, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Implement other roles similarly or restrict profile creation to Admin
        return Response({"detail": "Not implemented for this role"}, status=status.HTTP_501_NOT_IMPLEMENTED)


# Appointment Views

class DoctorListView(generics.ListAPIView):
    """List all doctors with their specializations and departments"""
    queryset = Doctor.objects.all()
    serializer_class = DoctorListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Doctor.objects.all()
        
        # Filter by department
        department = self.request.query_params.get('department', None)
        if department:
            queryset = queryset.filter(department_id=department)
        
        # Filter by specialization
        specialization = self.request.query_params.get('specialization', None)
        if specialization:
            queryset = queryset.filter(specialization__icontains=specialization)
        
        return queryset


class DoctorAvailabilityView(APIView):
    """Get available time slots for a specific doctor"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, pk):
        try:
            doctor = Doctor.objects.get(pk=pk)
        except Doctor.DoesNotExist:
            return Response(
                {"error": "Doctor not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get date from query params (required)
        date_str = request.query_params.get('date')
        if not date_str:
            return Response(
                {"error": "Date parameter is required (format: YYYY-MM-DD)"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get number of days to check (default 7)
        days = int(request.query_params.get('days', 7))
        
        # Get duration (default 30 minutes)
        duration = int(request.query_params.get('duration', 30))
        
        # Calculate available slots for each day
        from .utils import get_available_slots
        
        all_slots = []
        for day_offset in range(days):
            check_date = date + timedelta(days=day_offset)
            slots = get_available_slots(doctor, check_date, duration)
            
            for slot in slots:
                all_slots.append({
                    'start_time': slot,
                    'end_time': slot + timedelta(minutes=duration)
                })
        
        serializer = AvailableSlotSerializer(all_slots, many=True)
        return Response({
            'doctor': DoctorListSerializer(doctor).data,
            'duration': duration,
            'slots': serializer.data
        })


class AppointmentListCreateView(generics.ListCreateAPIView):
    """
    GET: List user's appointments (patients see their own, doctors see their schedule)
    POST: Create new appointment (patients only)
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AppointmentCreateSerializer
        return AppointmentSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        if user.role == 'PATIENT':
            try:
                patient = user.patient_profile
                queryset = Appointment.objects.filter(patient=patient)
            except Patient.DoesNotExist:
                queryset = Appointment.objects.none()
        elif user.role == 'DOCTOR':
            try:
                doctor = user.doctor_profile
                queryset = Appointment.objects.filter(doctor=doctor)
            except Doctor.DoesNotExist:
                queryset = Appointment.objects.none()
        elif user.role == 'ADMIN':
            queryset = Appointment.objects.all()
        else:
            queryset = Appointment.objects.none()
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter.upper()[0])
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d')
                queryset = queryset.filter(appointment_time__gte=start)
            except ValueError:
                pass
        
        if end_date:
            try:
                end = datetime.strptime(end_date, '%Y-%m-%d')
                queryset = queryset.filter(appointment_time__lte=end)
            except ValueError:
                pass
        
        return queryset.order_by('appointment_time')
    
    def perform_create(self, serializer):
        # Automatically set patient to current user's patient profile
        user = self.request.user
        
        if user.role != 'PATIENT':
            raise permissions.PermissionDenied("Only patients can create appointments")
        
        try:
            patient = user.patient_profile
            serializer.save(patient=patient)
        except Patient.DoesNotExist:
            raise permissions.PermissionDenied("Patient profile not found. Please complete your profile first.")


class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: View appointment details
    PUT/PATCH: Update appointment (status, notes) - doctors and admin only
    DELETE: Cancel appointment - patient (if >24hrs away) or admin
    """
    queryset = Appointment.objects.all()
    permission_classes = [IsAppointmentOwnerOrDoctor]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AppointmentUpdateSerializer
        return AppointmentSerializer
    
    def update(self, request, *args, **kwargs):
        # Only doctors and admins can update appointments
        if request.user.role not in ['DOCTOR', 'ADMIN']:
            return Response(
                {"error": "Only doctors and admins can update appointments"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        appointment = self.get_object()
        
        # Check if user can cancel
        can_cancel_permission = CanCancelAppointment()
        if not can_cancel_permission.has_object_permission(request, self, appointment):
            return Response(
                {"error": "You cannot cancel this appointment. Appointments must be cancelled at least 24 hours in advance."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Mark as cancelled instead of deleting
        appointment.status = 'X'
        appointment.save()
        
        return Response(
            {"message": "Appointment cancelled successfully"},
            status=status.HTTP_200_OK
        )


class MyAppointmentsView(generics.ListAPIView):
    """Convenience endpoint for patients to see their appointments"""
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        try:
            if user.role == 'PATIENT':
                patient = user.patient_profile
                queryset = Appointment.objects.filter(patient=patient)
            elif user.role == 'DOCTOR':
                doctor = user.doctor_profile
                queryset = Appointment.objects.filter(doctor=doctor)
            else:
                queryset = Appointment.objects.none()
        except (Patient.DoesNotExist, Doctor.DoesNotExist):
            queryset = Appointment.objects.none()
        
        # Filter by type
        filter_type = self.request.query_params.get('filter', None)
        
        if filter_type == 'upcoming':
            queryset = queryset.filter(
                appointment_time__gte=timezone.now(),
                status='S'
            )
        elif filter_type == 'past':
            queryset = queryset.filter(
                appointment_time__lt=timezone.now()
            )
        elif filter_type == 'cancelled':
            queryset = queryset.filter(status='X')
        
        return queryset.order_by('appointment_time')


# Medical Record / EHR Views

class MedicalRecordListCreateView(generics.ListCreateAPIView):
    """
    GET: List medical records (filtered by user role)
    POST: Create new medical record (doctors only)
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MedicalRecordCreateSerializer
        return MedicalRecordSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        if user.role == 'PATIENT':
            # Patients can only see their own records
            try:
                patient = user.patient_profile
                queryset = MedicalRecord.objects.filter(patient=patient)
            except Patient.DoesNotExist:
                queryset = MedicalRecord.objects.none()
        elif user.role == 'DOCTOR':
            # Doctors can see records they created
            try:
                doctor = user.doctor_profile
                queryset = MedicalRecord.objects.filter(doctor=doctor)
            except Doctor.DoesNotExist:
                queryset = MedicalRecord.objects.none()
        elif user.role in ['ADMIN', 'NURSE', 'RECEPTIONIST']:
            # Admin and staff can see all records
            queryset = MedicalRecord.objects.all()
        else:
            queryset = MedicalRecord.objects.none()
        
        # Filter by patient ID if provided
        patient_id = self.request.query_params.get('patient', None)
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        # Filter by doctor ID if provided
        doctor_id = self.request.query_params.get('doctor', None)
        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d').date()
                queryset = queryset.filter(visit_date__gte=start)
            except ValueError:
                pass
        
        if end_date:
            try:
                end = datetime.strptime(end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(visit_date__lte=end)
            except ValueError:
                pass
        
        return queryset.order_by('-visit_date', '-created_at')
    
    def perform_create(self, serializer):
        # Only doctors can create medical records
        user = self.request.user
        
        if user.role != 'DOCTOR':
            raise permissions.PermissionDenied("Only doctors can create medical records")
        
        try:
            doctor = user.doctor_profile
            # Save with audit trail
            serializer.save(doctor=doctor, created_by=user, updated_by=user)
        except Doctor.DoesNotExist:
            raise permissions.PermissionDenied("Doctor profile not found")


class MedicalRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: View medical record details
    PUT/PATCH: Update medical record (doctors only)
    DELETE: Delete medical record (admin only)
    """
    queryset = MedicalRecord.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return MedicalRecordUpdateSerializer
        return MedicalRecordSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        if user.role == 'PATIENT':
            # Patients can only see their own records
            try:
                patient = user.patient_profile
                return MedicalRecord.objects.filter(patient=patient)
            except Patient.DoesNotExist:
                return MedicalRecord.objects.none()
        elif user.role == 'DOCTOR':
            # Doctors can see records they created
            try:
                doctor = user.doctor_profile
                return MedicalRecord.objects.filter(doctor=doctor)
            except Doctor.DoesNotExist:
                return MedicalRecord.objects.none()
        elif user.role in ['ADMIN', 'NURSE', 'RECEPTIONIST']:
            # Admin and staff can see all records
            return MedicalRecord.objects.all()
        else:
            return MedicalRecord.objects.none()
    
    def update(self, request, *args, **kwargs):
        # Only doctors and admins can update medical records
        if request.user.role not in ['DOCTOR', 'ADMIN']:
            return Response(
                {"error": "Only doctors and admins can update medical records"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Update audit trail
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=request.user)
        
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        # Only admins can delete medical records
        if request.user.role != 'ADMIN':
            return Response(
                {"error": "Only admins can delete medical records"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


class PatientMedicalHistoryView(generics.RetrieveAPIView):
    """Get complete medical history for a specific patient"""
    queryset = Patient.objects.all()
    serializer_class = PatientMedicalHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.role == 'PATIENT':
            # Patients can only see their own history
            try:
                patient = user.patient_profile
                return Patient.objects.filter(id=patient.id)
            except Patient.DoesNotExist:
                return Patient.objects.none()
        elif user.role in ['DOCTOR', 'NURSE', 'ADMIN', 'RECEPTIONIST']:
            # Healthcare staff can see all patient histories
            return Patient.objects.all()
        else:
            return Patient.objects.none()

