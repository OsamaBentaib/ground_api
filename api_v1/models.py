from django.db import models

class Cities(models.Model):
    country = models.CharField(max_length=2,)
    name = models.CharField(max_length=200)
    lat = models.DecimalField(max_digits=10, decimal_places=5)
    lng = models.DecimalField(max_digits=10, decimal_places=5)

class Countries(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=2)



