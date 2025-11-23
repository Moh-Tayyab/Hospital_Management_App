from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Patient, Doctor, Nurse, Staff, Department

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', 'PATIENT')
        )
        return user

class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['age', 'gender', 'contact_info', 'medical_history']

class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['specialization', 'department', 'contact_info', 'schedule']

class NurseProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nurse
        fields = ['department', 'contact_info', 'shift']

class StaffProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['role', 'department', 'contact_info']

# Additional Serializers
from .models import Doctor, Appointment, MedicalRecord, Patient

class DoctorListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Doctor
        fields = ['id', 'user', 'specialization', 'department', 'contact_info', 'schedule']

class AvailableSlotSerializer(serializers.Serializer):
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    formatted_time = serializers.SerializerMethodField()

    def get_formatted_time(self, obj):
        if isinstance(obj['start_time'], str):
            start_time = datetime.strptime(obj['start_time'], '%Y-%m-%dT%H:%M:%SZ')
        else:
            start_time = obj['start_time']
            
        return start_time.strftime('%Y-%m-%d %H:%M %p')

class AppointmentSerializer(serializers.ModelSerializer):
    doctor_details = DoctorListSerializer(source='doctor', read_only=True)
    can_cancel = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor_details', 'appointment_time', 'status', 'notes', 'reason', 'duration', 'created_at', 'updated_at', 'can_cancel']
        read_only_fields = ['status', 'created_at', 'updated_at']

    def get_can_cancel(self, obj):
        time_until_appointment = obj.appointment_time - timezone.now()
        return time_until_appointment > timedelta(hours=24)

class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'appointment_time', 'reason', 'duration']

class AppointmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['status', 'notes']
        read_only_fields = ['status']

class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = ['id', 'patient', 'doctor', 'visit_date', 'visit_notes', 'diagnosis', 'prescriptions', 'lab_results', 'follow_up_required', 'follow_up_date', 'attachments', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class MedicalRecordCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = ['patient', 'visit_date', 'visit_notes', 'diagnosis', 'prescriptions', 'lab_results', 'follow_up_required', 'follow_up_date', 'attachments']

class MedicalRecordUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = ['visit_notes', 'diagnosis', 'prescriptions', 'lab_results', 'follow_up_required', 'follow_up_date', 'attachments']

class PatientMedicalHistorySerializer(serializers.ModelSerializer):
    medical_records = MedicalRecordSerializer(many=True, read_only=True)
    class Meta:
        model = Patient
        fields = ['id', 'user', 'age', 'gender', 'contact_info', 'medical_history', 'patient_type', 'medical_records']