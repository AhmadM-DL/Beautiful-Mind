from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Doctor, Patient, Note, hash_phone
from .validators import validate_phone_number

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True)

# PATIENT

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['medical_id', 'display_id', 'alias', 'gender', 'age', 'married', 'mental_illness_diagnostic', 'medications', 'smoke', 'weekly_sport_activity', 'occupation']
        write_only_fields = ['medical_id']
        


class PatientUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = ['alias', 'gender', 'age', 'married', 'mental_illness_diagnostic', 'medications', 'smoke', 'weekly_sport_activity', 'occupation']

class PatientLoginByPhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField()  
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
        medical_id = hash_phone(phone_number)
        if Patient.objects.filter(medical_id=medical_id).exists():
            raise serializers.ValidationError("Phone number already exists")
        user = User.objects.create_user(
            role="DOCTOR",
            password=password,
            username=username
        )
        return Doctor.objects.create(user=user, phone_number=phone_number, **validated_data)

# Note
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['note']