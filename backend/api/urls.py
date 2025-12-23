from django.urls import path
from .views import *

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    
    path('doctor/register', DoctorRegisterView.as_view(), name='doctor-register'),
    path('doctor/patient', DoctorCreateUpdatePatientView.as_view(), name='doctor-create-update-patient'),
    path('doctor/patients', DoctorPatientsList.as_view(), name='doctor-patients'),
]
