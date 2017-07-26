from django.conf.urls import url

from .views import get_profile, token_create, user_create

urlpatterns = [
    url(r'^$', user_create),
    url(r'^(?P<user_id>\d+)/$', get_profile),
    url(r'^tokens/$', token_create)
]
