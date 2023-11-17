from rest_framework import serializers
from .models import LoginCredentials

class LoginCredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginCredentials
        fields = ['username', 'password']