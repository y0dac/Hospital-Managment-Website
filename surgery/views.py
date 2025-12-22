# surgery/views.py
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from .serializer import PatientRegisterSerializer, DoctorRegisterSerializer,AppointmentSerializer , DoctorApproveAppointmentSerializer , appointmentCancelSerializer , slotsSerializer ,shiftSerializer,AvailableRoomSerializer,surgerycaseSerializer,doctorfinishedappointmentSerializer,doctordayappointmentSerializer,appointmentnoteSerializer,getnoteSerializer,patientdayappointmentSerializer,patientfinishedappointmentSerializer,addroomSerializer,PatientScanSerializer,PatientProfilePicSerializer,DoctorProfilePicSerializer,PatientProfileSerializer,DoctorProfileSerializer,DoctorPublicProfileSerializer,PatientPublicProfileSerializer
from .models import Appointment,Patient,Room,Doctor,Doctor_notes,Surgery,DoctorShift
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from .permissions import IsDoctor , IsPatient
from .services.appointments import start_end_shift_slots , auto_end_expired_appointments
from .services.roomslogic import availablerooms  , autofree
from django.utils.timezone import now





@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def patient_register(request):
    serializer = PatientRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def doctor_register(request):
    serializer = DoctorRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def appointmnet_booking(request):
    serializer = AppointmentSerializer(data=request.data, context={'request': request})

    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated  , IsDoctor])
def appointment_approval(request , pk , decision):
    auto_end_expired_appointments()
    print('appointment')
    appointment = get_object_or_404(Appointment, id = pk)
    serializer = DoctorApproveAppointmentSerializer(instance=appointment , data = {} , context ={'decision' : decision})
    serializer.is_valid()
    if request.user != appointment.doctor.user :
         return Response(serializer.errors, status= status.HTTP_403_FORBIDDEN)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([ IsAuthenticated ,IsPatient])
def appointment_cancel(request, pk):
    auto_end_expired_appointments()
    print("Appointment cancel view hit")
    print(request.user)
    appointment = get_object_or_404(Appointment, id=pk)
    serializer = appointmentCancelSerializer(instance=appointment, data={})
    serializer.is_valid()


    if request.user != appointment.patient.user:
        return Response(
            {"detail": "You are not allowed to cancel this appointment."},
            status=status.HTTP_403_FORBIDDEN
        )

    serializer = appointmentCancelSerializer(instance=appointment, data={})
    serializer.is_valid()
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)
@api_view(['GET'])
@permission_classes([ IsAuthenticated])

def availableslots(request,pk):
    auto_end_expired_appointments()
    date = request.query_params.get('date')
    if not date:
        return Response({"error": "Date parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    slots = start_end_shift_slots(pk ,date )
    serializer = slotsSerializer(slots , many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated ,IsDoctor ])
def shift_register(request):
    print(request.data)
    serializer = shiftSerializer(context = {'request' :request} , data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
@permission_classes([IsAuthenticated  , IsDoctor])
def surgeryrooms(request):#needs testing
    autofree()
    rooms = Room.objects.filter(is_available=True).prefetch_related('devices')
    if not rooms.exists() :
        return  Response("no data was found", status=status.HTTP_404_NOT_FOUND)

    serializer = AvailableRoomSerializer( rooms  , many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)
@api_view(['POST'])
@permission_classes([IsAuthenticated  , IsDoctor])
def surgery(request):#needs testing
    autofree()
    serializer = surgerycaseSerializer(data = request.data , context = {'request':request})
    
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
@permission_classes([ IsAuthenticated])
def getfinishedappointments(request):# needs testing
    appointment =  Appointment.objects.filter(doctor = request.user.doctor , 
                                              status = Appointment.StatusChoices.ENDED)
    serializer = doctorfinishedappointmentSerializer(appointment,many = True)
    return Response(serializer.data , status = status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([ IsAuthenticated])
def getdayappointment(request , pk): ## needs testing 
    today = now().today()
    doctor = Doctor.objects.get(id = pk)
    appointment = Appointment.objects.filter(doctor = doctor ,
       status = Appointment.StatusChoices.PENDING , 
       date = today)
    serializer = doctordayappointmentSerializer(appointment,many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)
@api_view(['POST'])
@permission_classes([IsAuthenticated  , IsDoctor])
def doctornote(request):
    autofree()
    serializer = appointmentnoteSerializer(data = request.data , context = {'request' : request})
    
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([ IsAuthenticated  , IsDoctor])
def getnote(request,pk):
    note = Doctor_notes.objects.filter(id = pk,
doctor__user=request.user
)
    serializer = getnoteSerializer(note ,many = True)
    return Response(serializer.data , status = status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([ IsAuthenticated])
def getpatientappointments(request , pk) :
    patient = Patient.objects.get(id =pk)
    appointments = Appointment.objects.filter(
        patient = patient,
        status__in = [Appointment.StatusChoices.APPROVED , Appointment.StatusChoices.PENDING]
    )
    serializer = patientdayappointmentSerializer(appointments , many = True)
    return Response(serializer.data , status = status.HTTP_200_OK)
@api_view(['GET'])
@permission_classes([ IsAuthenticated])
def getpatientfinishedappointment(request):
    user =request.user
    patient = Patient.objects.get(user = user)
    appointment = Appointment.objects.filter(patient = patient, 
                                             status = Appointment.StatusChoices.ENDED)
    serializer = patientfinishedappointmentSerializer(appointment,many = True)
    return Response(serializer.data , status = status.HTTP_200_OK)
@api_view(['POST'])
@permission_classes([IsAuthenticated  , IsDoctor])
def addroom(request):

    serializer = addroomSerializer(data = request.data )
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
 # views.py
@api_view([ 'POST'])
@permission_classes([IsAuthenticated, IsPatient])
def add_patient_scans(request):
    patient = request.user.patient

    if request.method == 'POST':
        serializer = PatientScanSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    scans = patient.scans.all()
    serializer = PatientScanSerializer(scans, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsPatient])
def upload_patient_profile_pic(request):
    patient = request.user.patient
    serializer = PatientProfilePicSerializer(
        patient, data=request.data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsDoctor])
def upload_doctor_profile_pic(request):
    doctor = request.user.doctor
    serializer = DoctorProfilePicSerializer(
        doctor, data=request.data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_profile(request):
    patient = getattr(request.user, "patient", None)
    if not patient:
        return Response({"detail": "This user is not a patient"}, status=404)
    serializer = PatientProfileSerializer(patient)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated , IsDoctor])
def doctor_profile(request):
    doctor = getattr(request.user, "doctor", None)
    if not doctor:
        return Response({"detail": "This user is not a doctor"}, status=404)
    serializer = DoctorProfileSerializer(doctor)
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsPatient])
def edit_patient_profile(request):
    patient = request.user.patient
    serializer = PatientProfileSerializer(
        patient, data=request.data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsDoctor])
def edit_doctor_profile(request):
    doctor = request.user.doctor
    serializer = DoctorProfileSerializer(
        doctor, data=request.data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

# surgery/views.py
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def doctor_public_profile(request, pk):
    doctor = get_object_or_404(Doctor, id=pk)

    serializer = DoctorPublicProfileSerializer(doctor)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsDoctor])
def patient_profile_for_doctor(request, pk):
    patient = get_object_or_404(Patient, id=pk)
    doctor = request.user.doctor

    has_appointment = Appointment.objects.filter(
        doctor=doctor,
        patient=patient
    ).exists()

    has_surgery = Surgery.objects.filter(
        doctor=doctor,
        patient=patient
    ).exists()

    if not (has_appointment or has_surgery):
        return Response(
            {"detail": "You are not allowed to view this patient."},
            status=status.HTTP_403_FORBIDDEN
        )

    serializer = PatientPublicProfileSerializer(patient)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsDoctor])
def patient_scans(request, pk):
    patient = get_object_or_404(Patient, id=pk)
    doctor = request.user.doctor

    allowed = Appointment.objects.filter(
        doctor=doctor,
        patient=patient
    ).exists() or Surgery.objects.filter(
        doctor=doctor,
        patient=patient
    ).exists()

    if not allowed:
        return Response(
            {"detail": "You are not allowed to view these scans."},
            status=status.HTTP_403_FORBIDDEN
        )

    scans = patient.scans.all()
    serializer = PatientScanSerializer(scans, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsDoctor])
def today_shift(request):
    doctor = request.user.doctor
    today = now().date()
    shifts = DoctorShift.objects.filter(doctor=doctor, date=today)
    serializer = shiftSerializer(shifts, many=True)
    return Response(serializer.data)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user

    if hasattr(user, "patient"):
        serializer = PatientProfileSerializer(user.patient)
        return Response({
            "role": "patient",
            "profile": serializer.data
        })

    if hasattr(user, "doctor"):
        serializer = DoctorProfileSerializer(user.doctor)
        return Response({
            "role": "doctor",
            "profile": serializer.data
        })

    return Response({"detail": "No profile found"}, status=404)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getalldoctors(request):
    doctors = Doctor.objects.all()
    serializer = DoctorProfileSerializer(doctors,many = True)
    return Response(serializer.data)