from django.urls import path

from .views import *


urlpatterns = [
    path('login', LoginView.as_view(), name='all_login'),
    
    path('doctor/register', DoctorRegisterView.as_view(), name='doctor-register'),
    path('doctor/patient', DoctorCreateUpdatePatientView.as_view(), name='doctor-create-update-patient'),
    path('doctor/patients', DoctorPatientsList.as_view(), name='doctor-patients'),


    path('patient/login-by-phone-number', PatientLoginByPhoneNumberView.as_view(), name='patient_login_by_phone_number'),
    path('patient/add-note', AddNoteView.as_view(), name='add_note'),
]

