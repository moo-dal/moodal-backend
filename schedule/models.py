from django.db import models

from accounts.models import User
# Create your models here.


class Schedule(models.Model):
    title = models.CharField(max_length=50)
    url = models.URLField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_shared = models.BooleanField()
    is_public = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
