from django.db import models
from django.contrib.auth.models import User
from .topic import Topic
from .abstract import Abstract


class Post(Abstract):
    body = models.CharField(max_length=1000)
    grade = models.IntegerField(default=0)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
