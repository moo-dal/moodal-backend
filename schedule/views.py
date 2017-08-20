from rest_framework import generics

from accounts.authentications import JWTAuthentication
from .serializers import PreferenceSerializer, ScheduleSerializer


class PreferenceCreate(generics.CreateAPIView):
    """
    관심사 공유달력을 추가합니다.
    calendar_ids 필드에는 , 로 구분된 calendar id 들을 문자열로 넣어주세요.
    """
    authentication_classes = (JWTAuthentication, )
    serializer_class = PreferenceSerializer


class ScheduleCreate(generics.CreateAPIView):
    """
    새로운 일정을 생성(추가)합니다
    """
    serializer_class = ScheduleSerializer
    authentication_classes = (JWTAuthentication, )
