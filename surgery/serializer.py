from rest_framework import serializers
from .models import CustomUser, Appointment, Patient, Doctor , DoctorShift , Room , RoomDevice , Surgery,Doctor_notes,PatientScan,RoleChoices

from dj_rest_auth.serializers import LoginSerializer
from datetime import date

# --------------------------
# Patient Registration
# --------------------------
class CustomloginSerializer(LoginSerializer):
        username = serializers.CharField(required=True)  # this will map to ssn


class PatientRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['ssn', 'name', 'password', 'birth_date', 'phone_number', 'sex']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Create the custom user
        user = CustomUser.objects.create_user(
            ssn=validated_data['ssn'],
            name=validated_data['name'],
            role='patient',
            password=validated_data['password'],
            birth_date=validated_data.get('birth_date'),
            phone_number=validated_data.get('phone_number'),
            sex=validated_data.get('sex')
        )

        # Create the patient profile
        Patient.objects.create(
            user=user,
            name=user.name,
            birth_date=user.birth_date,
            phonenumber=user.phone_number,
            sex=user.sex
        )

        return user


# --------------------------
# Doctor Registration
# --------------------------
class DoctorRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['ssn', 'name', 'password', 'birth_date', 'phone_number', 'sex', 'medical_license']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_medical_license(self, value):
        if not value or value.strip() == "":
            raise serializers.ValidationError("This field is required")
        return value

    def create(self, validated_data):
      medical_license = validated_data.get('medical_license')
      if not medical_license:
        raise serializers.ValidationError({"medical_license": "This field is required"})

    # Create CustomUser
      user = CustomUser.objects.create_user(
        ssn=validated_data['ssn'],
        name=validated_data['name'],
        role=RoleChoices.DOCTOR,
        password=validated_data['password'],
        birth_date=validated_data.get('birth_date'),
        phone_number=validated_data.get('phone_number'),
        sex=validated_data.get('sex'),
        medical_license=medical_license
    )

    # Create Doctor profile
      Doctor.objects.create(
        user=user,
        name=user.name,
        birth_date=user.birth_date,
        phonenumber=user.phone_number,
        sex=user.sex
    )

      return user





# --------------------------
# Appointment Serializer
# --------------------------
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['date', 'start', 'end', 'reason', 'doctor']

    def create(self, validated_data):
        user = self.context['request'].user
        patient = Patient.objects.get(user=user)  # Fixed capitalization
        validated_data['patient'] = patient
        return Appointment.objects.create(**validated_data)

    def validate(self, attrs):
        from datetime import datetime, time

        date_val = attrs.get('date')
        start_val = attrs.get('start')
        end_val = attrs.get('end')
        if isinstance(start_val, str):
           start_val = datetime.strptime(start_val, "%H:%M").time()
           end_val = attrs['end']
        if isinstance(end_val, str):
            end_val = datetime.strptime(end_val, "%H:%M").time()
        user = self.context['request'].user
        patient_obj = Patient.objects.get(user=user)
        appointments = Appointment.objects.filter(patient_id=str(patient_obj.id),
        status__in=[Appointment.StatusChoices.PENDING, Appointment.StatusChoices.APPROVED],
        date = date_val,
        start = start_val
        ,end =end_val           
        )
        if len(appointments) !=0:
             raise serializers.ValidationError("You already have an appointment in this time range.")
        return attrs

        
    
class DoctorApproveAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = []
               
    def update(self, instance, validated_data):
        if instance.status != Appointment.StatusChoices.PENDING:
            raise serializers.ValidationError('only pending can be approved')
        decision = self.context['decision'] 
        if decision == 'approve':
            instance.status = Appointment.StatusChoices.APPROVED
        elif decision == 'refuse':
            instance.status = Appointment.StatusChoices.REFUSE
        instance.save()
        return instance       

class appointmentCancelSerializer(serializers.ModelSerializer):
    class Meta :
        model = Appointment
        fields = []
    def update(self, instance, validated_data):
        if instance.status != Appointment.StatusChoices.PENDING and instance.status != Appointment.StatusChoices.APPROVED:
            raise serializers.ValidationError("can cancel appointments if it was compllected or canceled already")
        instance.status =  Appointment.StatusChoices.CANCELED
        instance.save()
        return instance
class slotsSerializer(serializers.Serializer):
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    status = serializers.CharField()    

class shiftSerializer(serializers.ModelSerializer):
    class Meta :
        model  = DoctorShift
        fields= ['start_time' , 'end_time' ,'date']  
    def create(self, validated_data):
        user = self.context['request'].user
        doctor = Doctor.objects.get(user = user)
        validated_data['doctor'] = doctor
        return DoctorShift.objects.create(**validated_data)
    
class DoctorProfileSerializer(serializers.ModelSerializer):
    clocked_in = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = [
            'id', 'name', 'email', 'birth_date',
            'phonenumber', 'sex', 'bio', 'profile_pic','clocked_in'
        ]
    def get_clocked_in(self, obj):
        today = localdate()
        # Make sure your DoctorShift model has related_name='shifts'
        return obj.shifts.filter(date=today).exists()   

from django.utils.timezone import localdate

class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            'id', 'name', 'email', 'birth_date',
            'phonenumber', 'sex', 'profile_pic'
        ]

class RoomDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomDevice
        fields = ['name']


class AvailableRoomSerializer(serializers.ModelSerializer):
    devices = RoomDeviceSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'devices']

class surgerycaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Surgery
        fields = ['patient','priority','type','date','room']
    def create(self, validated_data):
        user = self.context['request'].user
        doctor = Doctor.objects.get(user= user)
        validated_data['doctor'] = doctor
        room = validated_data['room']
        room.is_available = False

        room.save()
        
        return Surgery.objects.create(**validated_data)    

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'name']
class doctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'name']        

class doctorfinishedappointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    class Meta:
        model = Appointment
        fields=['date','patient','reason']
        
class doctordayappointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    class Meta:
        model = Appointment
        fields=['date','patient','reason']
class patientdayappointmentSerializer(serializers.ModelSerializer):
    doctor = doctorSerializer(read_only=True)
    class Meta:
        model = Appointment
        fields=['date','patient','reason','doctor']        
class patientfinishedappointmentSerializer(serializers.ModelSerializer):
    doctor = doctorSerializer(read_only=True)
    class Meta:
        model = Appointment
        fields=['date','patient','reason'] 
class appointmentnoteSerializer(serializers.ModelSerializer):
    class Meta:
        model =Doctor_notes
        fields = ['time','patient','note','appointment']
    def create(self, validated_data):
        user = self.context['request'].user
        doctor = Doctor.objects.get(user = user)
        validated_data['doctor'] = doctor
        return Doctor_notes.objects.create(**validated_data)
class appointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'patient','reason']        
    
class getnoteSerializer(serializers.ModelSerializer):
    appointment = appointmentSerializer(read_only = True)
    patient = PatientSerializer(read_only = True)
    class Meta:
        model  = Doctor_notes
        fields = ['time' , 'patient' , 'note' , 'appointment']

class addroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['name']
    def create(self, validated_data):
        return Room.objects.create(**validated_data)    
# serializers.py
class PatientScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientScan
        fields = ['id', 'image', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']

    def create(self, validated_data):
        user = self.context['request'].user
        patient = Patient.objects.get(user=user)
        validated_data['patient'] = patient
        return super().create(validated_data)
class PatientProfilePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['profile_pic']

class DoctorProfilePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['profile_pic']


class DoctorPublicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            'id',
            'name',
            'bio',
            'phonenumber',
            'email',
            'profile_pic',
        ]

class PatientPublicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            'id',
            'name',
            'birth_date',
            'sex',
            'phonenumber',
            'email',
            'profile_pic',
        ]
class PatientScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientScan
        fields = [
            'id',
            'image',
            'uploaded_at',
        ]                