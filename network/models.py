from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, date


class User(AbstractUser):
    followers = models.ManyToManyField(
        'self', symmetrical=False, related_name='following')


class Post(models.Model):
    poster = models.ForeignKey(
        'User', related_name='posts', on_delete=models.CASCADE)
    content = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    liker = models.ManyToManyField('User', related_name='likee')
