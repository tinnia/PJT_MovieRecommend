from django.db import models
from django.contrib.auth.models import AbstractUser
from movies.models import Rate

class User(AbstractUser):
    rates = models.ManyToManyField(Rate, related_name="users")
    karma = models.CharField(default=' ',max_length=40)