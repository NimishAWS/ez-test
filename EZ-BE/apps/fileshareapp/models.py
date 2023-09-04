from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date
from rest_framework_simplejwt.tokens import RefreshToken
from typing import Optional
from django.conf import settings
import time


# Create your models here.


class BaseModel(models.Model):
    """
    Base Model with created_at, and modified_at fields, will be inherited
    in all other models.
    """

    meta_created_ts = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="Meta Created TimeStamp",
        null=True,
        blank=True,
    )
    meta_updated_ts = models.DateTimeField(
        auto_now=True,
        db_index=True,
        verbose_name="Meta Updated TimeStamp",
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True

def user_doc(instance, filename):
    filebase, extension = filename.split(".")
    return "operational_user_doc/%s.%s" % (
        str(int(round(time.time() * 1000))),
        extension,
    )



class GUser(AbstractUser):
    """
    Captures  a user details and returns token
    """
    id = models.AutoField(primary_key=True)
    email = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        unique=True,
    )
    mobile = models.CharField(max_length=20, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    is_client = models.BooleanField(default=True)
    is_operation = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    created_date = models.DateField(default=date.today)
    modified_date = models.DateField(default=date.today)
    is_send_email = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "General Users"
        db_table = "general_user"

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


class UploadedFile(BaseModel):
    """
    Store User Uploaded files
    """
    user = models.ForeignKey(GUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_doc,blank=True,null=True)
    upload_datetime = models.DateTimeField(auto_now_add=True)
