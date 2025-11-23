from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'ADMIN'

class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'DOCTOR'

class IsNurse(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'NURSE'

class IsReceptionist(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'RECEPTIONIST'

class IsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'PATIENT'


# Appointment-specific permissions

class IsPatientOrAdmin(permissions.BasePermission):
    """Allow patients to create appointments, admins to manage all"""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role in ['PATIENT', 'ADMIN']


class IsAppointmentOwnerOrDoctor(permissions.BasePermission):
    """Allow appointment owner or assigned doctor to view/modify"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Admin can access all
        if request.user.role == 'ADMIN':
            return True
        
        # Patient can access their own appointments
        if request.user.role == 'PATIENT':
            try:
                return obj.patient.user == request.user
            except:
                return False
        
        # Doctor can access appointments assigned to them
        if request.user.role == 'DOCTOR':
            try:
                return obj.doctor.user == request.user
            except:
                return False
        
        return False


class CanCancelAppointment(permissions.BasePermission):
    """Check if user can cancel appointment (patient with >24hr notice or admin)"""
    def has_object_permission(self, request, view, obj):
        # Admin can always cancel
        if request.user.role == 'ADMIN':
            return True
        
        # Patient can cancel their own appointment if >24 hours away
        if request.user.role == 'PATIENT':
            try:
                if obj.patient.user == request.user:
                    return obj.can_cancel()
            except:
                return False
        
        return False
