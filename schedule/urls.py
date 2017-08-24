from django.conf.urls import url

from .views import CalendarList, PreferenceListCreate, ScheduleListCreate

urlpatterns = [
    url(r'^calendars$', CalendarList.as_view()),
    url(r'^preferences$', PreferenceListCreate.as_view()),
    url(r'^schedules$', ScheduleListCreate.as_view()),
]
