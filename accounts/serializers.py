import time

import jwt
from rest_framework import serializers

from .models import User

TOKEN_SECRET = "temp-secret"  # 배포 환경에서 config.py 등의 파일로 빼내고 VCS 에서 제거할 예정~
TOKEN_EXPIRY_MS = 1000 * 3600 * 3  # 3 hours. 변환해주는 라이브러리가 있으면 좋겠다.


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="pk", read_only=True)
    name = serializers.CharField(source="username")
    password_check = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "password", "name", "password_check")
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        if validated_data["password"] != validated_data["password_check"]:
            raise serializers.ValidationError("password mismatches")

        user = User()
        user.email = validated_data["email"]
        user.set_password(validated_data["password"])  # user.password = password 로 바로 assign 하면 안됨
        user.username = validated_data["username"]  # Django 에서 username 컬럼이 UNIQUE constraint -> 임시방편!
        user.save()
        return user


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(read_only=True)
    user = serializers.JSONField(read_only=True)

    def create(self, validated_data):
        user = User.objects.get(email=validated_data["email"])
        user.check_password(validated_data["password"])

        payload = {
            "email": validated_data["email"],
            "id": user.pk,
            "name": user.username,
            "expiry": int(time.time() * 1000) + TOKEN_EXPIRY_MS
        }

        instance = {
            "token": jwt.encode(payload=payload, key=TOKEN_SECRET).decode("utf-8"),
            "user": UserSerializer().to_representation(user)
        }

        return instance


class UserUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="username")

    class Meta:
        model = User
        fields = ("id", "name")
        extra_kwargs = {"name": {"write_only": True}}
