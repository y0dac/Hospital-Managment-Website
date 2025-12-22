from rest_framework_simplejwt.views import TokenObtainPairView
from .auth import SSNTokenObtainPairSerializer

class SSNTokenObtainPairView(TokenObtainPairView):
    serializer_class = SSNTokenObtainPairSerializer
