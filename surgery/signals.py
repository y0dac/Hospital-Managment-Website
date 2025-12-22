from  .models import Doctor , Appointment,Room
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import date , datetime
@receiver(post_save , sender = Appointment )
def auto_reject(sender, instance , created,**kwrgs):
    if instance.status != Appointment.StatusChoices.APPROVED:
        return

    Appointment.objects.filter(
        doctor=instance.doctor,
        date=instance.date,
        start=instance.start,
        end=instance.end,
        status=Appointment.StatusChoices.PENDING
    ).exclude(
        id=instance.id
    ).update(
        status=Appointment.StatusChoices.REFUSE
    )
    
