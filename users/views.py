import requests
import os
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response    
from rest_framework.decorators import APIView
from google.oauth2 import id_token
from google.auth.transport import requests
from django.db import models
from django.conf import settings
from rest_framework import generics

from orders.permissions import IsOwner
from orders.serializers import OrderSerializer
from users.serializers import AddressSerializer, OrderHistorySerializer
from .models import Address, OrderHistory

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

class OrderHistoryView(generics.ListAPIView):
    serializer_class = OrderHistorySerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return OrderHistory.objects.filter(user_id=self.request.COOKIES.get("uid"), order__status__in = ["delivered", "cancelled"]).order_by("-created_at")


class AddressListView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return Address.objects.filter(user_id=self.request.COOKIES.get("uid"))
    
    def create(self, request, *args, **kwargs):
        address_data = request.data
        address_data["user"] = User.objects.get(id=request.COOKIES.get("uid")) 
        serializer = AddressSerializer(data=address_data)
        if serializer.is_valid():
            serializer.save(user=address_data["user"])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AddressDetailView(generics.RetrieveUpdateDestroyAPIView): 
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return Address.objects.filter(user_id=self.request.COOKIES.get("uid"))
    
class SetDefaultAddressView(APIView):
    permission_classes = [IsOwner]

    def patch(self, request, pk):
        try:
            address = Address.objects.get(id=pk, user_id=request.COOKIES.get("uid"))
        except Address.DoesNotExist:
            return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)
        
        Address.objects.filter(user_id=request.COOKIES.get("uid"), is_default=True).update(is_default=False)
        address.is_default = True
        address.save()
        return Response({"message": "Default address updated"}, status=status.HTTP_200_OK)
    

           
        
