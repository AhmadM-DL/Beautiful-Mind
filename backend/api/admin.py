from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Patient, Doctor, Note

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_superuser')
    ordering = ('date_joined',)
    fieldsets = (
        (None, {'fields': ('password',)}),
        ('Personal info', {'fields': ('role',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'medical_id', 'age')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number')

@admin.register(Note)
class VoiceNoteAdmin(admin.ModelAdmin):
    list_display = ('patient', 'create_date')

