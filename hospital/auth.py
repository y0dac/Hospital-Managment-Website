from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class SSNTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "ssn"
