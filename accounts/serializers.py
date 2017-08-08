from rest_framework import serializers

from .models import User


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
