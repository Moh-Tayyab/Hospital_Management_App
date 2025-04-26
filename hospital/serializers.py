from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Department, Doctor, Nurse, Staff, Patient,
    Appointment, MedicalRecord
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name', 'description']

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    department = DepartmentSerializer(read_only=True)
    department_name = serializers.CharField(write_only=True)
    
    class Meta:
        model = Doctor
        fields = ['id', 'user', 'specialization', 'department', 'department_name', 'contact_info', 'schedule']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        department_name = validated_data.pop('department_name')
        
        # Create or get department - handle case where multiple departments exist
        try:
            department = Department.objects.get(name=department_name)
        except Department.DoesNotExist:
            department = Department.objects.create(name=department_name)
        except Department.MultipleObjectsReturned:
            # If multiple departments exist, use the first one
            department = Department.objects.filter(name=department_name).first()
        
        # Create user
        user = User.objects.create_user(**user_data)
        
        # Create doctor
        doctor = Doctor.objects.create(
            user=user,
            department=department,
            **validated_data
        )
        return doctor
    
    def update(self, instance, validated_data):
        # Update user data if provided
        if 'user' in validated_data:
            user_data = validated_data.pop('user')
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()
        
        # Update department if provided
        if 'department_name' in validated_data:
            department_name = validated_data.pop('department_name')
            department, _ = Department.objects.get_or_create(name=department_name)
            instance.department = department
        
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

class NurseSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    department = DepartmentSerializer()
    
    class Meta:
        model = Nurse
        fields = ['id', 'user', 'department', 'contact_info', 'shift']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        department_data = validated_data.pop('department')
        
        # Create or get department
        if 'id' in department_data:
            department = Department.objects.get(id=department_data['id'])
        else:
            department = Department.objects.create(**department_data)
        
        # Create user
        user = User.objects.create_user(**user_data)
        
        # Create nurse
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
    patient_id = serializers.IntegerField(write_only=True)
    doctor_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'patient_id', 'doctor_id', 'appointment_time', 'status', 'notes']
    
    def validate_patient_id(self, value):
        try:
            Patient.objects.get(id=value)
        except Patient.DoesNotExist:
            raise serializers.ValidationError("Patient with this ID does not exist.")
        return value
    
    def validate_doctor_id(self, value):
        try:
            Doctor.objects.get(id=value)
        except Doctor.DoesNotExist:
            raise serializers.ValidationError("Doctor with this ID does not exist.")
        return value
    
    def create(self, validated_data):
        patient_id = validated_data.pop('patient_id')
        doctor_id = validated_data.pop('doctor_id')
        
        patient = Patient.objects.get(id=patient_id)
        doctor = Doctor.objects.get(id=doctor_id)
        
        appointment = Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            **validated_data
        )
        return appointment

class MedicalRecordSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    
    class Meta:
        model = MedicalRecord
        fields = [
            'id', 'patient', 'doctor', 'diagnosis',
            'prescriptions', 'lab_results', 'created_at', 'updated_at'
        ] 