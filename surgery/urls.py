from django.urls import path
from .views import patient_register, doctor_register , appointmnet_booking ,appointment_approval , appointment_cancel,availableslots ,shift_register,surgeryrooms,surgery,getfinishedappointments,getdayappointment,doctornote,getnote,getpatientappointments,getpatientfinishedappointment,addroom,patient_scans,upload_patient_profile_pic,upload_doctor_profile_pic,patient_profile,doctor_profile,edit_patient_profile,edit_doctor_profile,doctor_public_profile,patient_profile_for_doctor,add_patient_scans,today_shift,me,getalldoctors

urlpatterns = [
    path('register/patient/', patient_register, name='patient-register'),
    path('register/doctor/', doctor_register, name='doctor-register'),
    path('appointment/', appointmnet_booking,name = 'appointment-booking'),
    path('appointmentDEC/<int:pk>/<str:decision>/' ,appointment_approval , name = 'appointment-decision'),
    path('appointment/<int:pk>/cancel/' , appointment_cancel , name = 'appointment-cancel') ,
    path('slots/<int:pk>/available/' , availableslots , name = 'availableslots' )
    ,path('shift/register/' , shift_register  , name = 'shift-register'),
    path('surgery/rooms/', surgeryrooms , name = 'surgery-rooms'),
    path('surgery/dec/' , surgery , name = 'surgery_dec'),
    path('appointment/finished/doctor/', getfinishedappointments , name = 'doctor_fininshed_appointments'),
    path('appointment/current/doctor' ,getdayappointment , name = 'doctor_current_appointments' ) , 
    path('appointment/note' , doctornote , name = 'doctor_note'),
    path('appointment/note/<int:pk>/' , getnote , name = "appointment_note"),
    path('appointment/patient/<int:pk>/' ,getpatientappointments , name = 'patient_appointments')
    ,path('appointment/patient/finished/' ,getpatientfinishedappointment, name = 'patient_finished_appointment'),
    path('add/room/' ,addroom , name='add_room'),
    path('patient/scans/', add_patient_scans),
path('patient/profile/pic/', upload_patient_profile_pic),
path('doctor/profile/pic/', upload_doctor_profile_pic),
path('patient/profile/', patient_profile),
path('doctor/profile/', doctor_profile),
path('patient/profile/edit/', edit_patient_profile),
path('doctor/profile/edit/', edit_doctor_profile),
path('doctors/<int:pk>/', doctor_public_profile),
    path('patients/<int:pk>/', patient_profile_for_doctor),
    path('patients/<int:pk>/scans/', patient_scans),
    path("shift/today/" ,today_shift ),path("me/", me),
    path('get/alldoctors/' , getalldoctors)


]
