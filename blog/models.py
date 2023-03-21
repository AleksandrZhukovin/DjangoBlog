from django.db import models
from django.contrib.auth.models import User


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
    grade = models.IntegerField(default=0)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Avatar(models.Model):
    id = models.IntegerField(primary_key=True)
    avatar = models.FileField(upload_to='static/avatars')
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Level(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.IntegerField(default=0)
    question = models.IntegerField(default=0)


class Like(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
