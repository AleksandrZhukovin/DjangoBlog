from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Topic(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    body = models.CharField(max_length=1000)
    time = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
