from rest_framework import serializers
from apps.fileshareapp.models import (
    GUser,
    UploadedFile
)
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
import re
import random

def generate_username(name):
    username = "".join(name.split(" ")).lower()
    if not GUser.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(1, 100))
        return generate_username(random_username)

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=6)
    password = serializers.CharField(max_length=255, min_length=6, write_only=True)

    class Meta:
        model = GUser
        fields = ["email", "first_name", "last_name", "password","is_operation"]

    def save(self):
        first_name = self.validated_data.get("first_name", " ")
        last_name = self.validated_data.get("last_name", " ")
        name = first_name + " " + last_name
        print(self.validated_data.get("is_operation"))
        user = GUser(
            email=self.validated_data["email"],
            first_name=first_name,
            last_name=last_name,
            password=self.validated_data["password"],
            username=generate_username(name),
            is_operation=self.validated_data.get("is_operation",False),
        )
        user.set_password(self.validated_data["password"])
        user.save()
        return user


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = GUser
        fields = ["token"]


class LoginSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=5)
    password = serializers.CharField(max_length=255, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, min_length=5, read_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = GUser.objects.get(email=obj["email"])
        return {"refresh": user.tokens()["refresh"], "access": user.tokens()["access"]}


    class Meta:
        model = GUser
        fields = ["email", "password", "tokens", "username" ]

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")

        user = authenticate(username=email, password=password)

        if not user:
            raise AuthenticationFailed("Invalid Credentials")
        if not user.is_active:
            raise AuthenticationFailed("Account disabled, please contact admin")
        if not user.is_verified:
            raise AuthenticationFailed("Email not verified, please check your email")
        # check password with regex
        if not re.match(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
            password,
        ):
            raise serializers.ValidationError(

                    "Password must contain at least 8 characters, 1 uppercase, 1 lowercase, 1 number and 1 special character"

            )

        return {"email": user.email, "username": user.username, "token": user.tokens()}
        return super().validate(attrs)



class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {"invalid_token": "Token is expired or invalid"}

    def validate(self, attrs):
        self.token = attrs.get("refresh")
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except Exception as e:
            self.fail("Invalid token")



class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ["id","user","file"]