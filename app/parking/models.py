from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.urls import reverse

# Create your models here.

class Parkings(models.Model):
    parkingName = models.CharField(max_length=50)
    description = models.TextField(blank=True)


    def __str__(self):
        return self.parkingName


    def get_absolute_url(self):
        return reverse('ParkingDetal', kwargs={'pk': self.pk})

class ParkingsTime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parkingName = models.ForeignKey(Parkings, on_delete=CASCADE)
    starDateTime = models.DateTimeField()
    stopDateTime = models.DateTimeField()


    def get_absolute_url(self):
        return reverse('ParkingAdd', kwargs={'pk': self.pk})

