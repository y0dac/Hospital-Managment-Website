from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.exceptions import ValidationError

class RoleChoices(models.TextChoices):
    PATIENT = 'patient', 'Patient'
    DOCTOR = 'doctor', 'Doctor'
    ADMIN = 'admin', 'Admin'

class CustomUserManager(BaseUserManager):
    class RoleChoices(models.TextChoices):
      PATIENT = 'patient', 'Patient'
      DOCTOR = 'doctor', 'Doctor'
      ADMIN = 'admin', 'Admin'
    def create_user(self, ssn, name, role, password=None, **extra_fields):
        if not ssn:
            raise ValueError("SSN must be provided")
        
        # Ensure medical license for doctors
        medical_license = extra_fields.get('medical_license')
        if role == RoleChoices.DOCTOR and not medical_license:
            raise ValueError("Doctors must have a medical license")
        
        user = self.model(ssn=ssn, name=name, role=role, **extra_fields)
        user.set_password(password)
        if role == RoleChoices.DOCTOR:
            user.is_staff = True  # optional
        user.save(using=self._db)
        return user

    def create_superuser(self, ssn, name, password=None, **extra_fields):
        user = self.create_user(
            ssn=ssn,
            name=name,
            role=RoleChoices.ADMIN,
            password=password,
            **extra_fields
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user



class CustomUser(AbstractBaseUser, PermissionsMixin):
    class RoleChoices(models.TextChoices):
      PATIENT = 'patient', 'Patient'
      DOCTOR = 'doctor', 'Doctor'
      ADMIN = 'admin', 'Admin'
    ssn = models.CharField(max_length=14, unique=True)
    name = models.CharField(max_length=50)
    role = models.CharField(max_length=10, choices=RoleChoices.choices)
    is_staff = models.BooleanField(default=False)
    medical_license = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    sex = models.CharField(max_length=1, choices=[('M','Male'),('F','Female')], blank=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'ssn'
    REQUIRED_FIELDS = ['name']

    def clean(self):
        if self.role == RoleChoices.DOCTOR and not self.medical_license:
            raise ValidationError("Doctors must have a medical license")

    def __str__(self):
        return f"{self.name} ({self.role})"

   

      
class SexChoices(models.TextChoices):
         MALE = 'M', 'Male'
         FEMALE = 'F', 'Female'
class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='patient',null=False)
    name = models.CharField(max_length=50)
    birth_date = models.DateField(null=True, blank=True)
    phonenumber= models.CharField(max_length=11)
    sex = models.CharField(max_length=1, choices=SexChoices.choices)
    profile_pic = models.ImageField(null=True)
    email = models.TextField(null= True)


    def __str__(self):
        return self.name
class PatientScan(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='scans')
    image = models.ImageField(upload_to='patients/scans/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
class Doctor(models.Model):
      profile_pic = models.ImageField(null=True)
      name = models.CharField(max_length=50)
      email = models.TextField(null= True)
      user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor' , null=False)
      birth_date = models.DateField(null=True, blank=True)
      sex = models.CharField(max_length=1, choices=SexChoices.choices)
      phonenumber= models.CharField(max_length=11)
      bio = models.TextField(null=True,blank=True)  
class StatusChoices(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        APPROVED = 'Approved', 'Approved'
        SCHEDULED = 'Scheduled', 'Scheduled'
        ENDED = 'Ended', 'Ended'
class Appointment(models.Model):
     class StatusChoices(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        APPROVED = 'Approved', 'Approved'
        REFUSE = 'Refuse' , 'Refuse'
        SCHEDULED = 'Scheduled', 'Scheduled'
        ENDED = 'Ended', 'Ended'
        CANCELED = 'Canceled','Canceled'

     date = models.DateField()
     patient = models.ForeignKey(Patient , on_delete=models.RESTRICT , related_name='appointments') 
     doctor = models.ForeignKey(Doctor,on_delete= models.RESTRICT , related_name= 'appointments')
     start = models.TimeField()
     end = models.TimeField()
     reason = models.TextField()
     status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING)
     created = models.DateTimeField(auto_now_add=True)
     
class Room(models.Model):
    name = models.CharField(max_length=50)   # OR-1, ICU-2, etc
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name     
class Surgery (models.Model):

     patient = models.ForeignKey(Patient,on_delete=models.RESTRICT) 
     doctor = models.ForeignKey(Doctor,on_delete=models.RESTRICT)
     priority = models.PositiveBigIntegerField()
     type = models.TextField()
     date = models.DateField(null=True)
     created=models.DateTimeField(auto_now_add=True)
     room = models.ForeignKey(Room, on_delete=models.PROTECT , null= True)
     def __str__(self):
        return f"Surgery {self.id} for {self.patient.name}"
     class Meta:
        unique_together = ('room', 'date')     
class Doctor_notes(models.Model):
      patient= models.ForeignKey(Patient,on_delete=models.RESTRICT)
      doctor = models.ForeignKey(Doctor,on_delete=models.RESTRICT)
      note = models.TextField()
      time = models.DateField()
      appointment=models.ForeignKey(Appointment,on_delete=models.RESTRICT)
     

class DoctorShift(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="shifts")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()



class RoomDevice(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="devices")
    name = models.CharField(max_length=100)  # "Ventilator", "ECG", "X-Ray"

    def __str__(self):
        return f"{self.room.name} - {self.name}"
