from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Doctor, Patient, VoiceNote, hash_phone
from .validators import validate_phone_number
User = get_user_model()

class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True)

# PATIENT

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['display_id', 'alias', 'gender', 'age', 'married', 'mental_illness_diagnostic', 'medications', 'smoke', 'weekly_sport_activity', 'occupation']

class PatientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['alias', 'gender', 'age', 'married', 'mental_illness_diagnostic', 'medications', 'smoke', 'weekly_sport_activity', 'occupation']

class PatientLoginByPhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField()  
    def validate_phone_number(self, value):
        return validate_phone_number(value)

class PatientLoginByPhoneNumberPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField()  
    password = serializers.CharField()
    def validate_phone_number(self, value):
        return validate_phone_number(value)

# DOCTOR

class DoctorSerializer(serializers.ModelSerializer):
    patients = PatientSerializer(many=True, read_only=True)    
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'patients']

class DoctorRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Doctor
        fields = ["username", "first_name", "last_name", "phone_number", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        username = validated_data.pop("username")
        username = username.lower()

        phone_number = validated_data.pop("phone_number")
        if Doctor.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError("Phone number already exists")
        if Patient.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError("Phone number already exists")

        user = User.objects.create_user(
            role="DOCTOR",
            password=password,
            username=username
        )
        return Doctor.objects.create(user=user, **validated_data)

# Voice Note

class VoiceNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceNote
        fields = ['medical_id', 'voice_note']