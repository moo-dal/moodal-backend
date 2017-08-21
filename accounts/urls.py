from django.conf.urls import url

from .views import TokenCreate, UserCreate, UserRetrieve

urlpatterns = [
    url(r'^$', UserCreate.as_view()),
    url(r'^(?P<user_id>\d+)/$', UserRetrieve.as_view()),
    url(r'^tokens/$', TokenCreate.as_view()),
]
