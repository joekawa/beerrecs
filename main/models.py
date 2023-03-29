from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class BREWERY(models.Model):
    name = models.TextField(max_length=100)
    description = models.TextField(max_length=500)
    city = models.TextField(max_length=50, null=True)
    state = models.TextField(max_length=50, null=True)
    country = models.TextField(max_length=50, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_date = models.DateTimeField(default=timezone.now)


class BEER(models.Model):
    name = models.TextField(max_length=40)
    description = models.TextField(max_length=500)
    brewery = models.ForeignKey(BREWERY, on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_date = models.DateTimeField(default=timezone.now)


class FAVORITE(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    beer = models.ForeignKey(BEER, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)


class TAG(models.Model):
    beer = models.ForeignKey(BEER, on_delete=models.CASCADE)
    tag = models.TextField(max_length=20)
    likes = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
