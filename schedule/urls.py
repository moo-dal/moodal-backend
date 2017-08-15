from django.conf.urls import url

from .views import ScheduleCreate

urlpatterns = [
    url(r'^create/$', ScheduleCreate.as_view()),
]