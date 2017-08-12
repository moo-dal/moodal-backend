import time

import jwt
from rest_framework import serializers

from .models import User

TOKEN_SECRET = "temp-secret"  # 배포 환경에서 config.py 등의 파일로 빼내고 VCS 에서 제거할 예정~
TOKEN_EXPIRY_MS = 1000 * 3600 * 3  # 3 hours. 변환해주는 라이브러리가 있으면 좋겠다.


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password", "nickname",)

    def create(self, validated_data):
        user = User()
        user.email = validated_data["email"]
        user.set_password(validated_data["password"])  # user.password = password 로 바로 assign 하면 안됨
        user.username = validated_data["email"]  # Django 에서 username 컬럼이 UNIQUE constraint -> 임시방편!
        user.save()
        return user

    def to_representation(self, instance):
        ret = {
            "id": instance.pk
        }
        return ret


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=50)  # max_length 는 별 의미 없음.

    def create(self, validated_data):
        user = User.objects.get(email=validated_data["email"])
        user.check_password(validated_data["password"])

        payload = {
            "email": validated_data["email"],
            "id": user.pk,
            "nickname": user.nickname,
            "expiry": int(time.time() * 1000) + TOKEN_EXPIRY_MS
        }

        resp = {
            "token": jwt.encode(payload=payload, key=TOKEN_SECRET).decode("utf-8"),
            "id": user.pk
        }

        return resp

    def to_representation(self, instance):
        return instance
