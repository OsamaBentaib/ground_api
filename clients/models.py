from django.db import models
from django.conf import settings
# Create your models here.


class Client(models.Model):
    user= models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    requestsNumber = models.IntegerField(default=0)
    requestsLimits = models.IntegerField(default=20000)
    lastRequest = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()
    link = models.CharField(max_length=200)
    addedAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)