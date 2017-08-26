from django.conf.urls import url

from .views import CalendarList, PreferenceListCreate, ScheduleCreate

urlpatterns = [
    url(r'^calendars$', CalendarList.as_view()),
    url(r'^schedules$', ScheduleCreate.as_view()),
    url(r'^preferences$', PreferenceListCreate.as_view()),
]
