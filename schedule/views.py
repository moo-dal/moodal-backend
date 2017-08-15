from rest_framework import generics

from .serializers import ScheduleSerializer


# Create your views here.

class ScheduleCreate(generics.CreateAPIView):
    """
    새로운 일정을 생성(추가)합니다
    """
    serializer_class = ScheduleSerializer
