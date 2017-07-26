from django.conf.urls import url

from .views import token_create, user_create

urlpatterns = [
    url(r'^$', user_create),
    url(r'^tokens/$', token_create)
]
