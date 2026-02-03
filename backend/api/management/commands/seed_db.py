import shortuuid
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models import Doctor, Patient, Note, hash_phone

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with a test doctor, a patient, and notes.'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # 1. Create a Doctor
        doctor_username = 'dr_john'
        doctor_phone = '12345678901'
        doctor_password = 'password123'

        if not User.objects.filter(username=doctor_username).exists():
            user_doctor = User.objects.create_user(
                role='DOCTOR',
                username=doctor_username,
                password=doctor_password
            )
            doctor_profile = Doctor.objects.create(
                user=user_doctor,
                phone_number=doctor_phone,
                first_name='John',
                last_name='Doe'
            )
            self.stdout.write(self.style.SUCCESS(f'Created Doctor: {doctor_username}'))
        else:
            user_doctor = User.objects.get(username=doctor_username)
            doctor_profile = user_doctor.doctor_profile
            self.stdout.write(f'Doctor {doctor_username} already exists.')

        # 2. Create a Patient
        patient_alias = 'Jane Smith'
        patient_phone = '98765432101'
        patient_password = "password123"
        medical_id = hash_phone(patient_phone)
        
        if not Patient.objects.filter(medical_id=medical_id).exists():
            patient_username = shortuuid.ShortUUID().random(length=12).lower()
            display_id = shortuuid.ShortUUID().random(length=12)
            
            user_patient = User.objects.create_user(
                role='PATIENT',
                username=patient_username,
                password=patient_password
            )
            patient_profile = Patient.objects.create(
                user=user_patient,
                medical_id=medical_id,
                display_id=display_id,
                alias=patient_alias,
                gender='F',
                age=30,
                married=False,
                mental_illness_diagnostic='Anxiety',
                occupation='Software Engineer'
            )
            
            # Link Patient to Doctor
            doctor_profile.patients.add(patient_profile)
            self.stdout.write(self.style.SUCCESS(f'Created Patient: {patient_alias} (linked to {doctor_username})'))
        else:
            patient_profile = Patient.objects.get(medical_id=medical_id)
            self.stdout.write(f'Patient {patient_alias} already exists.')

        # 3. Create a couple of Notes (messages)
        notes_content = [
        "انا اسمي شخص 5d08b0 انا بشتغل بمكان 439eef بمكان b0386c اليوم الصبح نزلت عالسيارة ورجعت طلعت عالبيت لقيت اكل انه سكرته بالمفتاح ونفس الشي بالنسبة لجنزير السيارة جنزير الموقف اتاكدت كذا مرة انه سكرته بس فتت عالسيارة غسلت ايدي كذا مرة بالوايبس ومشيت عالشغل"    
        ]

        if not Note.objects.filter(patient=patient_profile).exists():
            for content in notes_content:
                Note.objects.create(
                    patient=patient_profile,
                    note=content
                )
            self.stdout.write(self.style.SUCCESS(f'Created {len(notes_content)} notes for {patient_alias}.'))
        else:
            self.stdout.write(f'Notes for {patient_alias} already exist.')

        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))
