
from django.urls import path
from .views import (
    LoginAPIView,
    LogoutAPIView,
    RegisterView,
    VerifyEmail,
    FileUploadView,
    ListUploadedFilesView,
    FileDownloadView
)


urlpatterns = [

    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("email-verify/", VerifyEmail.as_view(), name="email-verify"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path('upload/', FileUploadView.as_view(), name='file_upload'),
    path('uploaded-files/', ListUploadedFilesView.as_view(), name='list_uploaded_files'),
    path('download/<int:file_id>/', FileDownloadView.as_view(), name='file_download'),

]
