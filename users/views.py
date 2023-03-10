from django.shortcuts import render
from django.contrib.auth import login, logout
from rest_framework import permissions
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework import generics
from . import serializers
from django.contrib.auth.models import User
# Login
class LoginView(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, format=None):
        try:
            serializer = serializers.LoginSerializer(data=self.request.data,context={'request': self.request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            login(request, user)
            return Response(None, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Logout function
class LogoutView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, format=None):
        logout(request)
        response = Response(None, status=status.HTTP_204_NO_CONTENT)
        response.set_cookie('sessionid', max_age=1, samesite='None')
        response.set_cookie('csrftoken', max_age=1, samesite='None')
        return response

####
class ProfileView(generics.RetrieveAPIView):
    serializer_class = serializers.UserSerializer
    def get_object(self):
        return self.request.user

# Register
# class RegisterView(views.APIView):
#     permission_classes = (permissions.AllowAny,)
#     def post(self, request, format=None):
#         serializer = serializers.UserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user.set_password(request.data['password']) # Add this line to save the password
#         user = serializer.save()
#         login(request, user)
#         return Response(None, status=status.HTTP_201_CREATED)
class RegisterView(views.APIView):
    def post(self, request):
        serializer = serializers.RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                serializer.validated_data['username'],
                serializer.validated_data['email'],
                serializer.validated_data['password']
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
