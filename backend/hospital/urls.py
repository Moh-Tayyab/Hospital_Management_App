from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    RegisterPatientView, RegisterStaffView, UserProfileView,
    DoctorListView, DoctorAvailabilityView,
    AppointmentListCreateView, AppointmentDetailView, MyAppointmentsView,
    MedicalRecordListCreateView, MedicalRecordDetailView, PatientMedicalHistoryView
)

urlpatterns = [
    # Authentication
    path('register/patient/', RegisterPatientView.as_view(), name='register_patient'),
    path('register/staff/', RegisterStaffView.as_view(), name='register_staff'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    
    # Doctors
    path('doctors/', DoctorListView.as_view(), name='doctor_list'),
    path('doctors/<int:pk>/availability/', DoctorAvailabilityView.as_view(), name='doctor_availability'),
    
    # Appointments
    path('appointments/', AppointmentListCreateView.as_view(), name='appointment_list_create'),
    path('appointments/my/', MyAppointmentsView.as_view(), name='my_appointments'),
    path('appointments/<int:pk>/', AppointmentDetailView.as_view(), name='appointment_detail'),
    
    # Medical Records / EHR
    path('medical-records/', MedicalRecordListCreateView.as_view(), name='medical_record_list_create'),
    path('medical-records/<int:pk>/', MedicalRecordDetailView.as_view(), name='medical_record_detail'),
    path('patients/<int:pk>/medical-history/', PatientMedicalHistoryView.as_view(), name='patient_medical_history'),
]