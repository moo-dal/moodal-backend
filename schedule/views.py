from django.db.models import Q
from rest_framework import generics

from accounts.authentications import JWTAuthentication
from .filters import ScheduleListFilter
from .models import Calendar, Schedule
from .serializers import CalendarSerializer, PreferenceSerializer, ScheduleSerializer


class CalendarList(generics.ListAPIView):
    # http://www.django-rest-framework.org/api-guide/generic-views/#examples
    """
    공유달력 목록을 조회합니다.
    """
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer


class PreferenceCreate(generics.CreateAPIView):
    """
    관심사 공유달력을 추가합니다.
    calendar_ids 필드에는 , 로 구분된 calendar id 들을 문자열로 넣어주세요.
    """
    authentication_classes = (JWTAuthentication, )
    serializer_class = PreferenceSerializer


class ScheduleListCreate(generics.ListCreateAPIView):
    """
    새로운 일정을 생성(추가)합니다
    """
    authentication_classes = (JWTAuthentication, )
    filter_backends = (ScheduleListFilter, )
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        # https://docs.djangoproject.com/en/1.11/ref/models/querysets/#year
        # https://docs.djangoproject.com/en/1.11/ref/models/querysets/#month
        # https://stackoverflow.com/a/3989905

        year_month = self.request.query_params["year_month"]
        year, month = year_month.split("-")

        queryset = Schedule.objects.filter((Q(start_date__year=year) & Q(start_date__month=month)) |
                                           (Q(end_date__year=year) & Q(end_date__month=month)))
        return queryset
