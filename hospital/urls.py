from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterPatientView, RegisterStaffView, UserProfileView

urlpatterns = [
    path('register/patient/', RegisterPatientView.as_view(), name='register_patient'),
    path('register/staff/', RegisterStaffView.as_view(), name='register_staff'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]