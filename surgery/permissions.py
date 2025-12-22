from rest_framework.permissions import BasePermission
from . models import Doctor,Patient
class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return Doctor.objects.filter(user=request.user).exists()

class IsPatient(BasePermission):
   def has_permission(self, request, view):
        if not request.user.is_authenticated:
           return False
    
        exists = Patient.objects.filter(user=request.user).exists()
        print("IsPatient check:", exists)   # <-- here
        return exists
