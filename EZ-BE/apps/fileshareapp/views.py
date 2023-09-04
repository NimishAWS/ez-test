from .serializers import (
    LogoutSerializer,
    RegisterSerializer,
    EmailVerificationSerializer,
    LoginSerializers,

)
from django.db import transaction

from apps.fileshareapp.models import (
    GUser,
    UploadedFile
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, status, views
from rest_framework.response import Response
from django.core.mail import send_mail
from apps.fileshareapp import constant
import jwt
from django.conf import settings
from django.template.loader import render_to_string

from django.contrib.sites.models import Site
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from rest_framework.parsers import FileUploadParser
from .serializers import UploadedFileSerializer


# Create your views here.


class RegisterView(generics.GenericAPIView):
    """
    Register a new user and send email to user for verification of email address

    """

    serializer_class = RegisterSerializer

    def post(self, request):
        try:
            with transaction.atomic():
                if GUser.objects.filter(email=request.data["email"]).exists():
                    return Response(
                        {
                            "status_code": status.HTTP_400_BAD_REQUEST,
                            "message": "Email already exists",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                user_request_data = request.data
                # create operationl user
                serializer = RegisterSerializer(data=user_request_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                user_data = serializer.data
                user = GUser.objects.get(email=user_data["email"])
                user_email = user.email
                token = RefreshToken.for_user(user).access_token
                if user_request_data.get('is_operation'):
                    user.is_verified = True
                    user.is_client = False
                    user.save()
                    return Response(
                        {
                        "status_code": status.HTTP_201_CREATED,
                        "message": "Operation user is created",
                        },
                        status=status.HTTP_201_CREATED,
                    )
                current_site = Site.objects.first()
                absurl = (
                        "http://" + current_site.domain + "/api/email-verify?token=" + str(token)
                )
                email_body = render_to_string(
                    constant.email_activation,
                    {
                        "first_name": user.username,
                        "absurl": absurl,
                    },
                )

                email_subject = constant.email_activation_subject
                from_email = settings.EMAIL_HOST_USER
                to_email = [user_email]
                send_email_to_user = send_mail(
                    email_subject,
                    email_body,
                    from_email,
                    to_email,
                    html_message=email_body,
                )
                return Response(
                    {
                        "status_code": status.HTTP_201_CREATED,
                        "message": "User is created Please verify your email to login",
                    },
                    status=status.HTTP_201_CREATED,
                )
        except Exception as e:
            return Response(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class VerifyEmail(views.APIView):
    """
    Verify email address of user and activate the user account
    """

    serializer_class = EmailVerificationSerializer
    # token paramerte configurations for email verification

    def get(self, request):
        token = request.GET.get("token")
        try:
            # We are passing our secret key here to decode the token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = GUser.objects.get(pk=payload["user_id"])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response(
                {
                    "status_code": status.HTTP_200_OK,
                    "message": "Successfully activated",
                },
                status=status.HTTP_200_OK,
            )
        except jwt.ExpiredSignatureError as identifier:
            return Response(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "Activation Expired",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except jwt.InvalidTokenError as identifier:
            return Response(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "Invalid Token",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class LoginAPIView(generics.GenericAPIView):
    """
    Login user and return access, refresh and user details
    """

    serializer_class = LoginSerializers

    def post(self, request):
        try:
            serializers = self.serializer_class(data=request.data)
            serializers.is_valid(raise_exception=True)
            return Response(
                {
                    "status_code": status.HTTP_200_OK,
                    "message": "User Logged in",
                    "data": serializers.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class LogoutAPIView(generics.GenericAPIView):
    """
    Logout user
    """
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(
                {"status_code": status.HTTP_200_OK, "message": "Logout Successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]  # Requires authentication to upload files

    def post(self, request, format=None):
        user_id = request.auth["user_id"]
        user_instance = GUser.objects.filter(pk=user_id).first()
        data = request.data
        data['user'] = user_id
        if not user_instance.is_operation:
            return Response(
                {
                    "status_code": status.HTTP_403_FORBIDDEN,
                    "error":"Access denied only operational user can upload files"},
                    status = status.HTTP_403_FORBIDDEN
            )

        file_serializer = UploadedFileSerializer(data=data)

        if file_serializer.is_valid():
            # Check if the uploaded file has a valid extension
            valid_extensions = ('.pptx', '.docx', '.xlsx')
            file_name = request.data['file'].name
            if not file_name.endswith(valid_extensions):
                return Response({
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    'error': 'Invalid file type. Only pptx, docx, and xlsx files are allowed.'
                }, status=status.HTTP_400_BAD_REQUEST)

            file_serializer.save(user=user_instance)  # Associate the file with the logged-in Ops User
            return Response({
                "status_code": status.HTTP_200_OK,
                'data': file_serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status_code": status.HTTP_400_BAD_REQUEST,
            'error': file_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


from django.core import signing
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class FileDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, file_id):
        try:
            # Check if the file exists and belongs to the logged-in Client User
            file_with_user_data = UploadedFile.objects.select_related('user').filter(pk=file_id).first()
            user_data = file_with_user_data.user
            print(user_data.email)
            if  file_with_user_data.user.is_client:
                return Response(
                    {
                        "status_code": status.HTTP_403_FORBIDDEN,
                        "error": "Access denied, Only client can download this file"},
                    status=status.HTTP_403_FORBIDDEN
                )

            # Generate a signed URL that includes the file ID
            signed_url = signing.dumps({'file': file_id})
            current_site = Site.objects.first()

            download_link = f'http://{current_site}/download-file/{signed_url}/'

            # Return the response with the download link
            response_data = {
                'message': 'success',
                'download-link': download_link
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except UploadedFile.DoesNotExist:
            return Response({
                "status_code": status.HTTP_400_BAD_REQUEST,
                'detail': 'File not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({  "status_code": status.HTTP_400_BAD_REQUEST,'detail': 'File not found'}, status=status.HTTP_404_NOT_FOUND)


class ListUploadedFilesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        files = UploadedFile.objects.all()
        serializer = UploadedFileSerializer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




