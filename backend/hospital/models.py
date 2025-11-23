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
    
    PATIENT_TYPE_CHOICES = [
        ('IN', 'In-Patient'),
        ('OUT', 'Out-Patient'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_profile')
    age: int = models.IntegerField()
    dob = models.DateField(null=True, blank=True, verbose_name='Date of Birth')
    gender: str = models.CharField(max_length=1, choices=GENDER_CHOICES)
    contact_info: str = models.CharField(max_length=100)
    
    # Medical History
    allergies: str = models.TextField(blank=True, help_text='Patient allergies')
    past_illnesses: str = models.TextField(blank=True, help_text='Past medical conditions and illnesses')
    medical_history: str = models.TextField(blank=True, help_text='General medical notes')
    
    # Patient Type
    patient_type: str = models.CharField(max_length=3, choices=PATIENT_TYPE_CHOICES, default='OUT')
    
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
    reason: str = models.TextField(blank=True, help_text='Reason for appointment')
    duration: int = models.IntegerField(default=30, help_text='Duration in minutes')
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)
    
    class Meta:
        # Prevent double-booking: same doctor cannot have overlapping appointments
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'appointment_time'],
                name='unique_doctor_appointment_time'
            )
        ]
        ordering = ['appointment_time']
    
    def __str__(self) -> str:
        return f"{self.patient} - {self.doctor} - {self.appointment_time}"
    
    def can_cancel(self) -> bool:
        """Check if appointment can be cancelled (must be >24 hours away)"""
        from django.utils import timezone
        from datetime import timedelta
        
        if self.status != 'S':
            return False
        
        time_until_appointment = self.appointment_time - timezone.now()
        return time_until_appointment > timedelta(hours=24)
    
    def is_upcoming(self) -> bool:
        """Check if appointment is in the future"""
        from django.utils import timezone
        return self.appointment_time > timezone.now() and self.status == 'S'

class MedicalRecord(models.Model):
    patient: 'Patient' = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    doctor: 'Doctor' = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='medical_records')
    
    # Visit Information
    visit_date: models.DateField = models.DateField(help_text='Date of the visit')
    visit_notes: str = models.TextField(help_text='Detailed notes from the visit')
    
    # Medical Details
    diagnosis: str = models.TextField(help_text='Diagnosis details')
    prescriptions: str = models.TextField(help_text='Prescribed medications and dosage')
    lab_results: str = models.TextField(blank=True, help_text='Laboratory test results')
    
    # Follow-up
    follow_up_required: bool = models.BooleanField(default=False, help_text='Does patient need follow-up?')
    follow_up_date: models.DateField = models.DateField(null=True, blank=True, help_text='Scheduled follow-up date')
    
    # Attachments (store file paths as JSON array)
    attachments: Dict[str, Any] = models.JSONField(
        default=list, 
        blank=True,
        help_text='List of attachment file paths/URLs'
    )
    
    # Audit Trail
    created_by: Optional['CustomUser'] = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='created_medical_records',
        help_text='User who created this record'
    )
    updated_by: Optional['CustomUser'] = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='updated_medical_records',
        help_text='User who last updated this record'
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-visit_date', '-created_at']
        indexes = [
            models.Index(fields=['patient', '-visit_date']),
            models.Index(fields=['doctor', '-visit_date']),
        ]
    
    def __str__(self) -> str:
        return f"Record for {self.patient} by {self.doctor} on {self.visit_date}"


# Billing Models

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('UNPAID', 'Unpaid'),
        ('PARTIALLY_PAID', 'Partially Paid'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    invoice_number: str = models.CharField(max_length=50, unique=True, editable=False)
    patient: 'Patient' = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='invoices')
    appointment: Optional['Appointment'] = models.ForeignKey(
        Appointment, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='invoices'
    )
    doctor: 'Doctor' = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='invoices')
    
    # Dates
    issue_date: models.DateField = models.DateField(auto_now_add=True)
    due_date: models.DateField = models.DateField()
    
    # Amounts
    total_amount: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_amount: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Status
    status: str = models.CharField(max_length=20, choices=STATUS_CHOICES, default='UNPAID')
    notes: str = models.TextField(blank=True)
    
    # Audit Trail
    created_by: Optional['CustomUser'] = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_invoices'
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['patient', '-created_at']),
            models.Index(fields=['status', '-created_at']),
        ]
    
    def save(self, *args, **kwargs):
        # Auto-generate invoice number if not set
        if not self.invoice_number:
            from django.utils import timezone
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            self.invoice_number = f"INV-{timestamp}"
        super().save(*args, **kwargs)
    
    def update_status(self):
        """Update invoice status based on payment amount"""
        if self.paid_amount >= self.total_amount:
            self.status = 'PAID'
        elif self.paid_amount > 0:
            self.status = 'PARTIALLY_PAID'
        else:
            # Check if overdue
            from django.utils import timezone
            if self.due_date < timezone.now().date() and self.status == 'UNPAID':
                self.status = 'OVERDUE'
        self.save()
    
    @property
    def balance(self) -> float:
        """Calculate remaining balance"""
        return float(self.total_amount - self.paid_amount)
    
    def __str__(self) -> str:
        return f"{self.invoice_number} - {self.patient} - ${self.total_amount}"


class InvoiceItem(models.Model):
    ITEM_TYPE_CHOICES = [
        ('CONSULTATION', 'Consultation Fee'),
        ('PROCEDURE', 'Medical Procedure'),
        ('MEDICATION', 'Medication'),
        ('LAB_TEST', 'Laboratory Test'),
        ('IMAGING', 'Imaging/Radiology'),
        ('ROOM_CHARGE', 'Room Charge'),
        ('OTHER', 'Other'),
    ]
    
    invoice: 'Invoice' = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description: str = models.CharField(max_length=200)
    item_type: str = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES, default='OTHER')
    quantity: int = models.IntegerField(default=1)
    unit_price: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        ordering = ['id']
    
    @property
    def total(self) -> float:
        """Calculate total for this line item"""
        return float(self.quantity * self.unit_price)
    
    def __str__(self) -> str:
        return f"{self.description} - ${self.total}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update invoice total
        self.invoice.total_amount = sum(item.total for item in self.invoice.items.all())
        self.invoice.save()


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('CASH', 'Cash'),
        ('CARD', 'Credit/Debit Card'),
        ('INSURANCE', 'Insurance'),
        ('ONLINE', 'Online Payment'),
        ('CHECK', 'Check'),
        ('OTHER', 'Other'),
    ]
    
    invoice: 'Invoice' = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    payment_method: str = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_id: str = models.CharField(max_length=100, blank=True)
    notes: str = models.TextField(blank=True)
    
    # Audit
    received_by: Optional['CustomUser'] = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='received_payments'
    )
    
    class Meta:
        ordering = ['-payment_date']
    
    def __str__(self) -> str:
        return f"Payment ${self.amount} for {self.invoice.invoice_number}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update invoice paid amount and status
        self.invoice.paid_amount = sum(payment.amount for payment in self.invoice.payments.all())
        self.invoice.update_status()

