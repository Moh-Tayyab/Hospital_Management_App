from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from typing import Optional, Dict, Any

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('DOCTOR', 'Doctor'),
        ('NURSE', 'Nurse'),
        ('RECEPTIONIST', 'Receptionist'),
        ('PATIENT', 'Patient'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='PATIENT')

    def __str__(self):
        return self.username

class Department(models.Model):
    name: str = models.CharField(max_length=100)
    description: str = models.TextField(blank=True)
    
    def __str__(self) -> str:
        return self.name

class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization: str = models.CharField(max_length=100)
    department: 'Department' = models.ForeignKey(Department, on_delete=models.CASCADE)
    contact_info: str = models.CharField(max_length=100)
    schedule: Dict[str, Any] = models.JSONField(default=dict)
    
    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"

class Nurse(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='nurse_profile')
    department: 'Department' = models.ForeignKey(Department, on_delete=models.CASCADE)
    contact_info: str = models.CharField(max_length=100)
    shift: str = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"

class Staff(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='staff_profile')
    role: str = models.CharField(max_length=100)
    department: 'Department' = models.ForeignKey(Department, on_delete=models.CASCADE)
    contact_info: str = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_profile')
    age: int = models.IntegerField()
    gender: str = models.CharField(max_length=1, choices=GENDER_CHOICES)
    contact_info: str = models.CharField(max_length=100)
    medical_history: str = models.TextField(blank=True)
    assigned_doctor: Optional['Doctor'] = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_nurse: Optional['Nurse'] = models.ForeignKey(Nurse, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('S', 'Scheduled'),
        ('C', 'Completed'),
        ('X', 'Cancelled'),
    ]
    
    patient: 'Patient' = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor: 'Doctor' = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_time: models.DateTimeField = models.DateTimeField()
    status: str = models.CharField(max_length=1, choices=STATUS_CHOICES, default='S')
    notes: str = models.TextField(blank=True)
    
    def __str__(self) -> str:
        return f"{self.patient} - {self.doctor} - {self.appointment_time}"

class MedicalRecord(models.Model):
    patient: 'Patient' = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor: 'Doctor' = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    diagnosis: str = models.TextField()
    prescriptions: str = models.TextField()
    lab_results: str = models.TextField(blank=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f"Record for {self.patient} by {self.doctor}"
