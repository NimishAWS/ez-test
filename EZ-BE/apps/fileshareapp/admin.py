from django.contrib import admin
from apps.fileshareapp.models import GUser,UploadedFile
# Register your models here.
admin.site.register(GUser)
admin.site.register(UploadedFile)


