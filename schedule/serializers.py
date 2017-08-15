import time

from rest_framework import serializers

from .models import Scheduling


class ScheduleSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    url = serializers.URLField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    is_shared = serializers.BooleanField()
    is_public = serializers.BooleanField()

    def create(self, validated_data):
        scheduling = Scheduling()
        scheduling.name = validated_data["name"]
        scheduling.url = validated_data["url"]
        scheduling.start_date = validated_data["start_date"]
        scheduling.end_date = validated_data["end_date"]
        scheduling.is_shared = validated_data["is_shared"]
        scheduling.is_public = validated_data["is_public"]
        scheduling.save()
        return scheduling

    def to_representation(self, instance):
        result = {
            "result": "success"
        }
        return result
