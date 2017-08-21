
from rest_framework import serializers

from .models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ("title", "url", "start_date", "end_date", "is_shared", "is_public", "user")
        #categori_name추가해야함
    '''
    모델 Serializer 를 상속하므로 상단처럼 하면 필드 자동 생성
    name = serializers.CharField(max_length=50)
    url = serializers.URLField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    is_shared = serializers.BooleanField()
    is_public = serializers.BooleanField()
    '''
    def create(self, validated_data):
        user_id = self.context['request'].user.id
        schedule = Schedule()
        schedule.title = validated_data["title"]
        schedule.url = validated_data["url"]
        schedule.start_date = validated_data["start_date"]
        schedule.end_date = validated_data["end_date"]
        schedule.is_shared = validated_data["is_shared"]
        schedule.is_public = validated_data["is_public"]
        schedule.user_id = user_id
        schedule.save()
        return schedule

    def to_representation(self, instance):
        result = {
            "result": "success"
        }
        return result
