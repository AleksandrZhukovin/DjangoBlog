from django.db import models
from django.contrib.auth.models import User


class Avatar(models.Model):
    file = models.FileField(upload_to='static/avatars')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
