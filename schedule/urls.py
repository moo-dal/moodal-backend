from django.conf.urls import url

from .views import ScheduleCreate

urlpatterns = [
    url(r'^$', ScheduleCreate.as_view()),
]