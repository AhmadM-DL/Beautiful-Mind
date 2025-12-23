from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from .models import Doctor, Patient, VoiceNote, hash_phone
from django.db.models import Q
from .serializers import *
import shortuuid

User = get_user_model()

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        identifier = serializer.validated_data['identifier']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(username=identifier)
        except User.DoesNotExist:
            try:
                doctor = Doctor.objects.get(phone_number=identifier)
                user = doctor.user
            except Doctor.DoesNotExist:
                try:
                    medical_id = hash_phone(identifier)
                    patient = Patient.objects.get(medical_id=medical_id)
                    user = patient.user
                except Patient.DoesNotExist:
                    return Response({'error': 'Invalid credentials'}, status=401)
        
        if not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=401)

        token = get_tokens_for_user(user).get('access')
        return Response({"token": token, "user": user.username, "role": user.role})

# PATIENT

class PatientLoginByPhoneNumberView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = PatientLoginByPhoneNumberSerializer(data=request.data)
        if serializer.is_valid():
            medical_id = hash_phone(serializer.validated_data['phone_number'])
            try:
                patient = Patient.objects.get(medical_id=medical_id)
                user = patient.user
                tokens = get_tokens_for_user(user)
                return Response(tokens)
            except Patient.DoesNotExist:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Doctor

class DoctorRegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        
        serializer = DoctorRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'status': 'Doctor registered'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoctorCreateUpdatePatientView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if not hasattr(request.user, 'doctor_profile'):
            return Response({'error': 'Not a doctor'}, status=status.HTTP_403_FORBIDDEN)

        phone_number = request.data.get('patient_phone_number')
        if not phone_number:
            return Response({'error': 'patient_phone_number is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        validate_phone_number(phone_number)

        medical_id = hash_phone(phone_number)

        if Patient.objects.filter(medical_id=medical_id).exists():
            return Response({'error': 'Patient already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        username = shortuuid.ShortUUID().random(length=12)
        username = username.lower()
        password = shortuuid.ShortUUID().random(length=12)
        display_id = shortuuid.ShortUUID().random(length=12)
        user = User.objects.create_user(role='PATIENT', username=username, password=password)
        patient_data = request.data.copy()
        patient_data['display_id'] = display_id
        serializer = PatientSerializer(data=patient_data)

        if serializer.is_valid():
            patient = serializer.save(user=user)
            request.user.doctor_profile.patients.add(patient)
            return Response({'status': 'Patient created'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        if not hasattr(request.user, 'doctor_profile'):
            return Response({'error': 'Not a doctor'}, status=status.HTTP_403_FORBIDDEN)

        display_id = request.data.get('patient_display_id')

        if not display_id:
            return Response({'error': 'patient_display_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            patient = Patient.objects.get(display_id=display_id)
        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PatientUpdateSerializer(patient, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Patient updated'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):

        if not hasattr(request.user, 'doctor_profile'):
            return Response({'error': 'Not a doctor'}, status=status.HTTP_403_FORBIDDEN)

        display_id = request.data.get('patient_display_id')
        if not display_id:
            return Response({'error': 'patient_display_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            patient = Patient.objects.get(display_id=display_id)
        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

        request.user.doctor_profile.patients.remove(patient)

        patient.user.delete()
        
        return Response({'status': 'Patient deleted'}, status=status.HTTP_200_OK)


class DoctorPatientsList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, 'doctor_profile'):
            return Response({'error': 'Not a doctor'}, status=status.HTTP_403_FORBIDDEN)
        
        patients = request.user.doctor_profile.patients.all()
        serializer = PatientSerializer(patients, many=True)
        data = serializer.data
        return Response(data)