from django.db import models
from django.contrib.auth.models import User
from typing import Optional, Dict, Any

class Department(models.Model):
    name: str = models.CharField(max_length=100)
    description: str = models.TextField(blank=True)
    
    def __str__(self) -> str:
        return self.name

class Doctor(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization: str = models.CharField(max_length=100)
    department: 'Department' = models.ForeignKey(Department, on_delete=models.CASCADE)
    contact_info: str = models.CharField(max_length=100)
    schedule: Dict[str, Any] = models.JSONField(default=dict)
    
    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"

class Nurse(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)
    department: 'Department' = models.ForeignKey(Department, on_delete=models.CASCADE)
    contact_info: str = models.CharField(max_length=100)
    shift: str = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"

class Staff(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)
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
    
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)
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
