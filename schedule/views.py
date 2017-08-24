from django.db.models import Q
from rest_framework import generics

from accounts.authentications import JWTAuthentication
from .filters import ScheduleListFilter
from .models import Calendar, Preference, Schedule
from .serializers import CalendarSerializer, PreferenceSerializer, ScheduleSerializer, MappingSerializer


class ScheduleListCreate(generics.ListCreateAPIView):
    """
    새로운 일정을 생성하고 조회합니다.
    
    [생성]
    
    start_date / end_date 는 yyyy-MM-dd 포맷으로 넘겨주세요.
    
    공유 달력 일정 추가일 경우 calendar_id 파라미터를 넘기고, 개인 달력 일정 추가일 경우 넘기지 않습니다.
    
    [조회]
        
    calendar_id / user_id 파라미터는 둘 중 하나를+하나만 꼭 넘겨줘야합니다.
    
    공유 달력을 조회하는 경우 -> calendar_id 파라미터
    
    개인 달력을 조회하는 경우 -> user_id 파라미터 
    """
    serializer_class = ScheduleSerializer
    authentication_classes = (JWTAuthentication, )
    filter_backends = (ScheduleListFilter, )

    def get_queryset(self):
        # https://docs.djangoproject.com/en/1.11/ref/models/querysets/#year
        # https://docs.djangoproject.com/en/1.11/ref/models/querysets/#month
        # https://stackoverflow.com/a/3989905

        year_month = self.request.query_params["year_month"]
        year, month = year_month.split("-")

        queryset = Schedule.objects.filter((Q(start_date__year=year) & Q(start_date__month=month)) |
                                           (Q(end_date__year=year) & Q(end_date__month=month)))
        return queryset


class CalendarList(generics.ListAPIView):
    # http://www.django-rest-framework.org/api-guide/generic-views/#examples
    """
    공유달력 목록을 조회합니다.
    """
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer


class PreferenceListCreate(generics.ListCreateAPIView):
    """
    관심사 공유달력을 추가하고 조회합니다.
    """
    authentication_classes = (JWTAuthentication, )
    serializer_class = PreferenceSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return Preference.objects.filter(user_id=user_id)


class MappingCreate(generics.CreateAPIView):
    """
    공유 달력의 일정을 개인 달력으로 가져옵니다.
    """
    authentication_classes = (JWTAuthentication, )
    serializer_class = MappingSerializer


class ScheduleRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    개인 달력의 일정을 공유 달력에 추가할때 / 일정을 삭제할때 사용합니다.
    
    현재는 calendar_id 파라미터만 처리합니다.
    나머지 파라미터들은 기존과 동일한 값을 올려줘야 합니다.
    """
    authentication_classes = (JWTAuthentication, )
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return Schedule.objects.filter(user_id=user_id)
