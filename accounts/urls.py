from django.conf.urls import url

from .views import ProfileRetrieve, TokenCreate, UserCreate

urlpatterns = [
    url(r'^$', UserCreate.as_view()),
    url(r'^(?P<user_id>\d+)/$', ProfileRetrieve.as_view()),
    url(r'^tokens/$', TokenCreate.as_view()),
]
