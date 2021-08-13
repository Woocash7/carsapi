from django.db import models
from django.db.models.fields.related import ForeignKey

# Create your models here.
class Car(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.make} | {self.model}'

class Rate(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='rates')
    rating = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.car.model} | {self.rating}'
