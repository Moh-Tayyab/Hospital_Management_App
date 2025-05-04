from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import (
    Department, Doctor, Nurse, Staff, Patient,
    Appointment, MedicalRecord
)
from .serializers import (
    DepartmentSerializer, DoctorSerializer, NurseSerializer,
    StaffSerializer, PatientSerializer, AppointmentSerializer,
    MedicalRecordSerializer, UserSerializer
)

def home(request):
    return render(request, 'hospital/home.html', {
        'title': 'Hospital Management System',
        'message': 'Welcome to the Hospital Management System API'
    })

# Create your views here.

class LoginView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']  # Explicitly allow PATCH
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response([{'name': item['name']} for item in serializer.data])
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'name': serializer.data['name']})
    
    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        if name:
            if Department.objects.filter(name=name).exists():
                return Response(
                    {'error': f'Department with name "{name}" already exists'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        response = super().create(request, *args, **kwargs)
        return Response({'name': response.data['name']}, status=status.HTTP_201_CREATED)
    
    def partial_update(self, request, *args, **kwargs):
        current_name = request.data.get('current_name')
        new_name = request.data.get('new_name')
        
        if not current_name or not new_name:
            return Response(
                {'error': 'Both current_name and new_name are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Check if department with current name exists
            departments = Department.objects.filter(name=current_name)
            if not departments.exists():
                return Response(
                    {'error': f'Department with name "{current_name}" does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Check if new name already exists
            if Department.objects.filter(name=new_name).exists():
                return Response(
                    {'error': f'Department with name "{new_name}" already exists'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Update all departments with the current name
            count = departments.count()
            departments.update(name=new_name)
            
            return Response({
                'current_name': current_name,
                'new_name': new_name,
                'message': f'Successfully updated {count} department(s) from "{current_name}" to "{new_name}"'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({'name': response.data['name']})
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        name = instance.name
        self.perform_destroy(instance)
        return Response({'name': name}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['delete'])
    def delete_by_name(self, request):
        name = request.data.get('name')
        if not name:
            return Response(
                {'error': 'Department name is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            departments = Department.objects.filter(name=name)
            count = departments.count()
            
            if count == 0:
                return Response(
                    {'name': name, 'message': f'Successfully deleted {count} department(s) with name {name}'},
                    status=status.HTTP_200_OK
                )
            
            # Delete all departments with the given name
            departments.delete()
            return Response(
                {'name': name, 'message': f'Successfully deleted {count} department(s) with name {name}'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def format_doctor_data(self, doctor):
        return {
            "id": doctor.id,
            "name": f"{doctor.user.first_name} {doctor.user.last_name}".strip(),
            "department": doctor.department.name,
            "contact_info": doctor.contact_info,
            "schedule": doctor.schedule
        }
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        formatted_data = [self.format_doctor_data(doctor) for doctor in queryset]
        return Response(formatted_data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        formatted_data = self.format_doctor_data(instance)
        return Response(formatted_data)
    
    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            doctor = Doctor.objects.get(id=response.data['id'])
            formatted_data = self.format_doctor_data(doctor)
            return Response(formatted_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            doctor = Doctor.objects.get(id=response.data['id'])
            formatted_data = self.format_doctor_data(doctor)
            return Response(formatted_data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def partial_update(self, request, *args, **kwargs):
        try:
            response = super().partial_update(request, *args, **kwargs)
            doctor = Doctor.objects.get(id=response.data['id'])
            formatted_data = self.format_doctor_data(doctor)
            return Response(formatted_data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'])
    def patients(self, request, pk=None):
        doctor = self.get_object()
        patients = Patient.objects.filter(assigned_doctor=doctor)
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def appointments(self, request, pk=None):
        doctor = self.get_object()
        appointments = Appointment.objects.filter(doctor=doctor)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

class NurseViewSet(viewsets.ModelViewSet):
    queryset = Nurse.objects.all()
    serializer_class = NurseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def format_nurse_data(self, nurse):
        return {
            "id": nurse.id,
            "name": f"{nurse.user.first_name} {nurse.user.last_name}".strip(),
            "department": {
                "name": nurse.department.name,
                "floor": nurse.department.description
            },
            "contact_info": nurse.contact_info,
            "shift": nurse.shift
        }
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        formatted_data = [self.format_nurse_data(nurse) for nurse in queryset]
        return Response(formatted_data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        formatted_data = self.format_nurse_data(instance)
        return Response(formatted_data)
    
    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            nurse = Nurse.objects.get(id=response.data['id'])
            formatted_data = self.format_nurse_data(nurse)
            return Response(formatted_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            nurse = Nurse.objects.get(id=response.data['id'])
            formatted_data = self.format_nurse_data(nurse)
            return Response(formatted_data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def partial_update(self, request, *args, **kwargs):
        try:
            response = super().partial_update(request, *args, **kwargs)
            nurse = Nurse.objects.get(id=response.data['id'])
            formatted_data = self.format_nurse_data(nurse)
            return Response(formatted_data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'])
    def patients(self, request, pk=None):
        nurse = self.get_object()
        patients = Patient.objects.filter(assigned_nurse=nurse)
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def format_staff_data(self, staff):
        return {
            "id": staff.id,
            "name": f"{staff.user.first_name} {staff.user.last_name}".strip(),
            "department": {
                "name": staff.department.name,
                "floor": staff.department.description
            },
            "contact_info": staff.contact_info,
            "role": staff.role
        }
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        formatted_data = [self.format_staff_data(staff) for staff in queryset]
        return Response(formatted_data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        formatted_data = self.format_staff_data(instance)
        return Response(formatted_data)
    
    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            staff = Staff.objects.get(id=response.data['id'])
            formatted_data = self.format_staff_data(staff)
            return Response(formatted_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            staff = Staff.objects.get(id=response.data['id'])
            formatted_data = self.format_staff_data(staff)
            return Response(formatted_data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def partial_update(self, request, *args, **kwargs):
        try:
            response = super().partial_update(request, *args, **kwargs)
            staff = Staff.objects.get(id=response.data['id'])
            formatted_data = self.format_staff_data(staff)
            return Response(formatted_data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']  # Explicitly allow PATCH
    
    def format_patient_data(self, patient):
        return {
            "id": patient.id,
            "name": f"{patient.user.first_name} {patient.user.last_name}".strip(),
            "age": patient.age,
            "gender": patient.gender,
            "contact_info": patient.contact_info,
            "medical_history": patient.medical_history,
            "assigned_doctor": {
                "id": patient.assigned_doctor.id,
                "name": f"{patient.assigned_doctor.user.first_name} {patient.assigned_doctor.user.last_name}".strip()
            } if patient.assigned_doctor else None,
            "assigned_nurse": {
                "id": patient.assigned_nurse.id,
                "name": f"{patient.assigned_nurse.user.first_name} {patient.assigned_nurse.user.last_name}".strip()
            } if patient.assigned_nurse else None
        }
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        formatted_data = [self.format_patient_data(patient) for patient in queryset]
        return Response(formatted_data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        formatted_data = self.format_patient_data(instance)
        return Response(formatted_data)
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            patient = Patient.objects.get(id=serializer.data['id'])
            formatted_data = self.format_patient_data(patient)
            return Response(formatted_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            patient = Patient.objects.get(id=serializer.data['id'])
            formatted_data = self.format_patient_data(patient)
            return Response(formatted_data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    @action(detail=True, methods=['get'])
    def appointments(self, request, pk=None):
        patient = self.get_object()
        appointments = Appointment.objects.filter(patient=patient)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def medical_records(self, request, pk=None):
        patient = self.get_object()
        records = MedicalRecord.objects.filter(patient=patient)
        serializer = MedicalRecordSerializer(records, many=True)
        return Response(serializer.data)

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    
    def format_appointment_data(self, appointment):
        return {
            "id": appointment.id,
            "patient": {
                "id": appointment.patient.id,
                "name": f"{appointment.patient.user.first_name} {appointment.patient.user.last_name}".strip(),
                "age": appointment.patient.age,
                "gender": appointment.patient.gender,
                "contact_info": appointment.patient.contact_info
            },
            "doctor": {
                "id": appointment.doctor.id,
                "name": f"{appointment.doctor.user.first_name} {appointment.doctor.user.last_name}".strip(),
                "department": appointment.doctor.department.name,
                "contact_info": appointment.doctor.contact_info
            },
            "appointment_date": appointment.appointment_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "status": appointment.status,
            "notes": appointment.notes
        }
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        formatted_data = [self.format_appointment_data(appointment) for appointment in queryset]
        return Response(formatted_data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        formatted_data = self.format_appointment_data(instance)
        return Response(formatted_data)
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            appointment = Appointment.objects.get(id=serializer.data['id'])
            formatted_data = self.format_appointment_data(appointment)
            return Response(formatted_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            appointment = Appointment.objects.get(id=serializer.data['id'])
            formatted_data = self.format_appointment_data(appointment)
            return Response(formatted_data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user.doctor)
