from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Department, Doctor, Nurse, Staff, Patient,
    Appointment, MedicalRecord
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'description']

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    department = DepartmentSerializer()
    
    class Meta:
        model = Doctor
        fields = ['id', 'user', 'specialization', 'department', 'contact_info', 'schedule']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        department_data = validated_data.pop('department')
        
        user = User.objects.create(**user_data)
        department = Department.objects.get(id=department_data['id'])
        
        doctor = Doctor.objects.create(user=user, department=department, **validated_data)
        return doctor

class NurseSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    department = DepartmentSerializer()
    
    class Meta:
        model = Nurse
        fields = ['id', 'user', 'department', 'contact_info', 'shift']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        department_data = validated_data.pop('department')
        
        user = User.objects.create(**user_data)
        department = Department.objects.get(id=department_data['id'])
        
        nurse = Nurse.objects.create(user=user, department=department, **validated_data)
        return nurse

class StaffSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    department = DepartmentSerializer()
    
    class Meta:
        model = Staff
        fields = ['id', 'user', 'role', 'department', 'contact_info']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        department_data = validated_data.pop('department')
        
        user = User.objects.create(**user_data)
        department = Department.objects.get(id=department_data['id'])
        
        staff = Staff.objects.create(user=user, department=department, **validated_data)
        return staff

class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    assigned_doctor = DoctorSerializer(read_only=True)
    assigned_nurse = NurseSerializer(read_only=True)
    
    class Meta:
        model = Patient
        fields = [
            'id', 'user', 'age', 'gender', 'contact_info',
            'medical_history', 'assigned_doctor', 'assigned_nurse'
        ]
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        patient = Patient.objects.create(user=user, **validated_data)
        return patient

class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'appointment_time', 'status', 'notes']

class MedicalRecordSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    
    class Meta:
        model = MedicalRecord
        fields = [
            'id', 'patient', 'doctor', 'diagnosis',
            'prescriptions', 'lab_results', 'created_at', 'updated_at'
        ] 