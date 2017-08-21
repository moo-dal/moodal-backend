from django.conf.urls import url

from .views import CalendarList, ScheduleListCreate

urlpatterns = [
    url(r'^calendars$', CalendarList.as_view()),
    url(r'^schedules$', ScheduleListCreate.as_view()),
]
