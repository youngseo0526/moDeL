import reserve as reserve
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse



class Photo(models.Model):
    photo = models.ImageField(upload_to="image")
    ratio = models.DecimalField(max_digits=5, decimal_places=2, null=True)




