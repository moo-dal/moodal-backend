from django.conf.urls import url

from .views import ScheduleCreate

urlpatterns = [
    url(r'^schedules$', ScheduleListCreate.as_view()),
]
