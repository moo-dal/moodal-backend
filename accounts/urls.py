from django.conf.urls import url

from .views import profile_detail, token_create, user_create

urlpatterns = [
    url(r'^$', user_create),
    url(r'^(?P<user_id>\d+)/$', profile_detail),
    url(r'^tokens/$', token_create),
]
