from django.db import models

from accounts.models import User
# Create your models here.


class Calendar(models.Model):
    title = models.CharField(max_length=50)


class Preference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)


class Schedule(models.Model):
    title = models.CharField(max_length=50)
    url = models.URLField()
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, null=True)


class Mapping(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=True)
