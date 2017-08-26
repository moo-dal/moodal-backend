from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from .models import Calendar, Mapping, Preference, Schedule, User


class ScheduleSerializer(serializers.ModelSerializer):
    calendar_id = serializers.IntegerField()
    is_public = serializers.BooleanField(write_only=True)
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Schedule
        fields = ("id", "title", "url", "start_date", "end_date", "calendar_id", "user_id", "is_public")
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
        user = User.objects.get(pk=user_id)
        schedule.user = user

        calendar_id = validated_data["calendar_id"]
        if calendar_id > 0:
            calendar = Calendar.objects.get(pk=calendar_id)
            schedule.calendar = calendar

        schedule.save()

        # calendar_id = 0 ~ 개인 달력의 일정 ~ is_public 을 고려해서 Mapping 테이블에 레코드 추가
        if calendar_id == 0:
            is_public = validated_data.get("is_public", True)
            Mapping.objects.create(user=user, schedule=schedule, is_public=is_public)

        return schedule


class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = "__all__"


class PreferenceSerializer(serializers.Serializer):
    calendar_id = serializers.IntegerField()
    user_id = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        calendar_id = validated_data["calendar_id"]
        user_id = self.context['request'].user.id

        try:
            return Preference.objects.get(calendar_id=calendar_id, user_id=user_id)
        except ObjectDoesNotExist:
            calendar = Calendar.objects.get(pk=calendar_id)
            user = User.objects.get(pk=user_id)
            return Preference.objects.create(calendar=calendar, user=user)


class MappingSerializer(serializers.Serializer):
    is_public = serializers.BooleanField()
    schedule_id = serializers.IntegerField()

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        schedule_id = validated_data["schedule_id"]
        is_public = validated_data["is_public"]
        mapping = Mapping.objects.create(user_id=user_id, schedule_id=schedule_id, is_public=is_public)
        return mapping
