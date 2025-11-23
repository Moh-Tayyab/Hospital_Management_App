from django.shortcuts import render
from rest_framework import generics, status, permissions

def home(request):
    return render(request, 'hospital/home.html', {
        'title': 'Hospital Management System',
        'message': 'Welcome to the Hospital Management System API'
    })
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import (
    RegisterSerializer, UserSerializer, 
    PatientProfileSerializer, DoctorProfileSerializer, 
    NurseProfileSerializer, StaffProfileSerializer
)
from .models import Patient, Doctor, Nurse, Staff
from .permissions import IsAdmin, IsDoctor, IsPatient

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
            profile, created = Patient.objects.get_or_create(user=user)
            serializer = PatientProfileSerializer(profile, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Implement other roles similarly or restrict profile creation to Admin
        return Response({"detail": "Not implemented for this role"}, status=status.HTTP_501_NOT_IMPLEMENTED)
