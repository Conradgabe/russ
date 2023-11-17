from django.shortcuts import render
from django.http import Http404

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from dotenv import load_dotenv
from passlib.context import CryptContext

import json, requests, os

from .models import LoginCredentials
from .serializers import LoginCredentialsSerializer

load_dotenv()

LOGIN_URL = os.getenv('LOGIN_URL')
SUB = os.getenv('SUB')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Create your views here.
class SyncCredentials(APIView):
    """
    Sync credentials from website to chatbot
    """

    # Get the username in database
    def get_object_username(self, username):
        try:
            return LoginCredentials.objects.filter(username=username).first()
        except LoginCredentials.DoesNotExist:
            raise Http404
        
    def post(self, request, format=None):
        session = requests.Session()
        # Get the login credentials for the user
        try:
            username = request.data['username']
            password = request.data['password']
        except Exception as e:
            return Response({'error_message': "fields should contain only username and password"})

        loginUser_data = {
            'login': username, 'pass': password, 'sub': SUB
            }
        
        response = session.post(LOGIN_URL, data=loginUser_data, allow_redirects=True)

        if response.status_code == 200:
            if 'Your password has expired.' in response.text:
                db_username = self.get_object_username(username)

                if not db_username:
                    serializer = LoginCredentialsSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()

                        return Response({'message': 'Success','status': status.HTTP_200_OK})
                else:
                    serializer = LoginCredentialsSerializer(db_username, data=request.data)
                    if serializer.is_valid():
                        serializer.save()

                        return Response({
                                'message': 'User new Credentials updated on chatbot', 'status': status.HTTP_200_OK
                            })
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Invalid Credentials',  'status': status.HTTP_401_UNAUTHORIZED})
        else:
            return Response({'message': 'Invalid Credentials',  'status': response.status_code})