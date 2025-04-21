from django.contrib import admin
from .models import (
    Department, Doctor, Nurse, Staff, Patient,
    Appointment, MedicalRecord
)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'department', 'contact_info')
    list_filter = ('department', 'specialization')
    search_fields = ('user__first_name', 'user__last_name', 'specialization')

@admin.register(Nurse)
class NurseAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'shift', 'contact_info')
    list_filter = ('department', 'shift')
    search_fields = ('user__first_name', 'user__last_name')

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'department', 'contact_info')
    list_filter = ('department', 'role')
    search_fields = ('user__first_name', 'user__last_name', 'role')

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'gender', 'assigned_doctor', 'assigned_nurse')
    list_filter = ('gender', 'assigned_doctor', 'assigned_nurse')
    search_fields = ('user__first_name', 'user__last_name')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_time', 'status')
    list_filter = ('status', 'appointment_time', 'doctor')
    search_fields = ('patient__user__first_name', 'patient__user__last_name', 'doctor__user__first_name')

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'created_at')
    list_filter = ('created_at', 'doctor')
    search_fields = ('patient__user__first_name', 'patient__user__last_name', 'doctor__user__first_name')
