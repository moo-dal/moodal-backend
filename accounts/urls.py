from django.conf.urls import url

from .views import profile_detail, token_create, UserCreate

urlpatterns = [
    url(r'^$', UserCreate.as_view()),
    url(r'^(?P<user_id>\d+)/$', profile_detail),
    url(r'^tokens/$', token_create),
]
