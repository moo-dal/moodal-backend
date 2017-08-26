from rest_framework import generics

from accounts.authentications import JWTAuthentication
from .serializers import CalendarSerializer, PreferenceSerializer, ScheduleSerializer
from .models import Calendar, Preference


# Create your views here.

class ScheduleCreate(generics.CreateAPIView):
    """
    새로운 일정을 생성(추가)합니다
    """
    serializer_class = ScheduleSerializer
    authentication_classes = (JWTAuthentication, )


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
