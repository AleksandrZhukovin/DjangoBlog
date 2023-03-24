from django.db import models
from django.contrib.auth.models import User
from .abstract import Abstract


class Topic(Abstract):
    name = models.CharField(max_length=100)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
