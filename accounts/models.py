from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    class Meta(object):
        unique_together = ('email',)

    nickname = models.CharField(max_length=100)
