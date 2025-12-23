import uuid
import hmac
import hashlib
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings
from django.utils import timezone
from .validators import validate_phone_number

def hash_phone(phone: str) -> str:
    return hmac.new(
        key=settings.PHONE_HASH_SECRET.encode(),
        msg=phone.encode(),
        digestmod=hashlib.sha256
    ).hexdigest()

class UserManager(BaseUserManager):
    def create_user(self, role, password=None, **extra_fields):
        if not role:
            raise ValueError('The Role must be set')
        user = self.model(role=role, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, password=None, **extra_fields):
        # Admin doesn't really have a phone number in this schema, or maybe just a generic role
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(role='ADMIN', password=password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100, unique=True)

    ROLE_CHOICES = (
        ("PATIENT", "Patient"),
        ("DOCTOR", "Doctor"),
        ("ADMIN", "Admin"),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.username)

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    medical_id = models.CharField(max_length=128, unique=True)
    display_id = models.CharField(max_length=128, unique=True)
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    alias = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.IntegerField()
    married = models.BooleanField(default=False)
    mental_illness_diagnostic = models.TextField(blank=True)
    medications = models.TextField(blank=True, help_text="List of medications")
    smoke = models.BooleanField(default=False)
    weekly_sport_activity = models.TextField(blank=True)
    occupation = models.TextField(blank=True)

    def __str__(self):
        return f"Patient {self.id}"

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    phone_number = models.CharField(max_length=20, unique=True, validators=[validate_phone_number])
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    patients = models.ManyToManyField(Patient, blank=True, related_name='doctors')

    def __str__(self):
        return self.user.username

class VoiceNote(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='voice_notes')
    note = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note for {self.patient} at {self.create_date}"
