from django.db import models
from django.contrib.auth.models import User


class Level(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.IntegerField(default=0)
    question = models.IntegerField(default=0)
