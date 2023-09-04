from django.apps import AppConfig


class FileshareappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.fileshareapp'


#
#
#
# Creating a complete secure file-sharing system using Django REST framework (DRF) with the specified requirements would involve several components and a substantial amount of code. Below, I'll provide you with a simplified example to get you started. Please note that this example does not cover all security aspects, and you should enhance it for production use.
#
# Step 1: Set Up Django Project
#
# First, create a Django project and a DRF app.
#
# bash
# Copy code
# # Create a new Django project
# django-admin startproject file_sharing
#
# # Create a new DRF app
# python manage.py startapp file_api
# Step 2: Define Models
#
# In your file_api app, define models for users and files. You can use Django's built-in User model and create a custom model for files.
#
# python
# Copy code
# # file_api/models.py
# from django.db import models
# from django.contrib.auth.models import User
#
# class File(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     file = models.FileField(upload_to='uploads/')
#     file_type = models.CharField(max_length=10)  # pptx, docx, xlsx
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#
# class ClientUser(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     encrypted_url = models.CharField(max_length=255, unique=True)
#
# # Implement email verification if needed
# Step 3: Create Serializers
#
# Define serializers to convert model instances to JSON and validate data.
#
# python
# Copy code
# # file_api/serializers.py
# from rest_framework import serializers
# from .models import File, ClientUser
#
# class FileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = File
#         fields = '__all__'
#
# class ClientUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ClientUser
#         fields = '__all__'
# Step 4: Create Views
#
# Define views and API endpoints for your actions.
#
# python
# Copy code
# # file_api/views.py
# from rest_framework import generics, permissions
# from .models import File, ClientUser
# from .serializers import FileSerializer, ClientUserSerializer
# from .permissions import IsClientUser, IsOpsUser
#
# class FileUploadView(generics.CreateAPIView):
#     serializer_class = FileSerializer
#     permission_classes = [permissions.IsAuthenticated, IsOpsUser]
#     # Implement file type validation
#
# class ClientUserSignUpView(generics.CreateAPIView):
#     serializer_class = ClientUserSerializer
#
# class ClientUserLoginView(generics.CreateAPIView):
#     # Implement client user login logic
#
# class FileDownloadView(generics.RetrieveAPIView):
#     queryset = File.objects.all()
#     serializer_class = FileSerializer
#     permission_classes = [permissions.IsAuthenticated, IsClientUser]
#
# class ListUploadedFilesView(generics.ListAPIView):
#     queryset = File.objects.all()
#     serializer_class = FileSerializer
#     permission_classes = [permissions.IsAuthenticated, IsOpsUser]
# Step 5: Define Permissions
#
# Create custom permissions for Ops User and Client User.
#
# python
# Copy code
# # file_api/permissions.py
# from rest_framework import permissions
#
# class IsOpsUser(permissions.BasePermission):
#     def has_permission(self, request, view):
#         # Implement Ops User check
#
# class IsClientUser(permissions.BasePermission):
#     def has_permission(self, request, view):
#         # Implement Client User check
# Step 6: Configure URLs
#
# Configure URLs for your API endpoints.
#
# python
# Copy code
# # file_sharing/urls.py
# from django.urls import path, include
#
# urlpatterns = [
#     path('api/', include('file_api.urls')),
# ]
# Step 7: Run Migrations
#
# Run database migrations to create the necessary database tables.
#
# bash
# Copy code
# python manage.py makemigrations
# python manage.py migrate
# Step 8: Write Test Cases
#
# Write test cases for your views and API endpoints using Django's testing framework.
#
# Step 9: Deployment
#
# For deployment, you can choose a web hosting platform such as Heroku, AWS, or a VPS provider. Set up a production-ready database, configure a production web server, and use environment variables to store sensitive information securely. Implement HTTPS for secure communication. Deploy using a production-ready WSGI server like Gunicorn.
#
# Please remember that this is a simplified example, and you should consider security, error handling, and performance optimization for a production system. Additionally, implementing email verification and secure file storage would require additional code and configuration.
#



