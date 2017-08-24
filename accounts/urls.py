from django.conf.urls import url

from .views import TokenCreate, UserCreate, TokenValidate, UserUpdate

urlpatterns = [
    url(r'^$', UserCreate.as_view()),
    url(r'^(?P<pk>\d+)/$', UserUpdate.as_view()),
    url(r'^tokens/$', TokenCreate.as_view()),
    url(r'^tokens/validate/$', TokenValidate.as_view())
]
