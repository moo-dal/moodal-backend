from django.conf.urls import url

from .views import CalendarList, PreferenceListCreate, ScheduleListCreate, MappingCreate, ScheduleRetrieveUpdateDestroy

urlpatterns = [
    url(r'^calendars$', CalendarList.as_view()),
    url(r'^preferences$', PreferenceListCreate.as_view()),
    url(r'^schedules$', ScheduleListCreate.as_view()),
    url(r'^schedule/(?P<pk>\d+)/$', ScheduleRetrieveUpdateDestroy.as_view()),
    url(r'^mapping$', MappingCreate.as_view()),
]
