from ..models import Doctor, Appointment ,DoctorShift
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta

def start_end_shift_slots(doctor_id, date):
    slots = []
    doc = get_object_or_404(Doctor , id = doctor_id)
    shift = get_object_or_404(DoctorShift, doctor=doc , date = date)
    fmt = "%H:%M:%S"

    # convert shift start/end to datetime objects
    starttime = datetime.strptime(str(shift.start_time), fmt)
    end_shift = datetime.strptime(str(shift.end_time), fmt)

    shift_hours = int((end_shift - starttime).total_seconds() // 3600)
    one_hour = timedelta(hours=1)

    for _ in range(shift_hours):
        endtime = starttime + one_hour

        # filter appointments for this slot
        appointment = Appointment.objects.filter(
            doctor=doc,
            date=date,
            start=starttime.time(),
            end=endtime.time(),
            status__in=[Appointment.StatusChoices.APPROVED, Appointment.StatusChoices.ENDED]
        )

        slots.append({
            'start_time': starttime.time(),
            'end_time': endtime.time(),
            'status': 'used' if appointment.exists() else 'free'
        })

        # move to next slot
        starttime = endtime

    return slots

from django.utils.timezone import now

def auto_end_expired_appointments():
    today = now().date()
    current_time = now().time()

    Appointment.objects.filter(
        date=today,
        end__lte=current_time,
        status=Appointment.StatusChoices.APPROVED
    ).update(status=Appointment.StatusChoices.ENDED)
