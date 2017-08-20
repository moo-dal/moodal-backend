from django.conf.urls import url

from .views import PreferenceCreate, ScheduleCreate

urlpatterns = [
    url(r'^calendars$', CalendarList.as_view()),
    url(r'^preferences$', PreferenceCreate.as_view()),
    url(r'^schedules$', ScheduleCreate.as_view()),
]