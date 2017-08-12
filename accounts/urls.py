from django.conf.urls import url

from .views import profile_detail, TokenCreate, UserCreate

urlpatterns = [
    url(r'^$', UserCreate.as_view()),
    url(r'^(?P<user_id>\d+)/$', profile_detail),
    url(r'^tokens/$', TokenCreate.as_view()),
]
