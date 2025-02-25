import requests
import os
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response    
from rest_framework.decorators import APIView
from google.oauth2 import id_token
from google.auth.transport import requests

User = get_user_model()


class LoginView(APIView):
    def post(self, request):
        try:
            token = request.data.get('token')
            # Specify the WEB_CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), os.getenv('GOOGLE_CLIENT_ID'))

            # Or, if multiple clients access the backend server:
            # idinfo = id_token.verify_oauth2_token(token, requests.Request())
            # if idinfo['aud'] not in [WEB_CLIENT_ID_1, WEB_CLIENT_ID_2, WEB_CLIENT_ID_3]:
            #     raise ValueError('Could not verify audience.')

            # If the request specified a Google Workspace domain
            # if idinfo['hd'] != DOMAIN_NAME:
            #     raise ValueError('Wrong domain name.')

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            userid = idinfo['sub']
            email = idinfo['email']
            name = idinfo['name']
            picture = idinfo['picture']
            given_name = idinfo['given_name']
            family_name = idinfo['family_name']

            user, created = User.objects.get_or_create(email=email, defaults={'first_name': given_name, 'last_name': family_name, 'profile_picture': picture})

            response = Response({
                "email": user.email,
                "name": user.first_name
            }, status=status.HTTP_201_CREATED)

            response.set_cookie('uid', user.id)
            return response
        

            # return Response({
            #     "email": user.email,
            #     "name": user.first_name
            # }, status=status.HTTP_201_CREATED)    
        
        except Exception as e:
            # Invalid token
            print(e)
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


           
        
