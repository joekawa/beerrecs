from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class BREWERY(models.Model):
    name = models.TextField(max_length=100)
    description = models.TextField(max_length=500)
    city = models.TextField(max_length=50, null=True)
    state = models.TextField(max_length=50, null=True)
    country = models.TextField(max_length=50, null=True)


class BEER(models.Model):
    name = models.TextField(max_length=40)
    description = models.TextField(max_length=500)
    brewery = models.ForeignKey(BREWERY, on_delete=models.CASCADE, null=True)


class FAVORITE(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    beer = models.ForeignKey(BEER, on_delete=models.CASCADE)