from django.conf.urls import url

from .views import CalendarList, PreferenceCreate, ScheduleListCreate

urlpatterns = [
    url(r'^calendars$', CalendarList.as_view()),
    url(r'^preferences$', PreferenceCreate.as_view()),
    url(r'^schedules$', ScheduleListCreate.as_view()),
]
