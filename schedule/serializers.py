
from rest_framework import serializers

from .models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    calendar_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    class Meta:
        model = Schedule
        fields = ("title", "url", "start_date", "end_date", "calendar_id", "user_id")
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
        schedule = Schedule()
        schedule.title = validated_data["title"]
        schedule.url = validated_data["url"]
        schedule.start_date = validated_data["start_date"]
        schedule.end_date = validated_data["end_date"]

        user_id = self.context['request'].user.id
        calendar_id = validated_data["calendar_id"]
        user = User.objects.get(pk=user_id)
        calendar = Calendar.objects.get(pk=calendar_id)

        schedule.user = user
        schedule.calendar = calendar

        schedule.save()

        return schedule
