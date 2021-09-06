from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from customers.models import *
# Create your models here.


class City(models.Model):
    city_name = models.CharField(max_length=30)
    zip_code = models.IntegerField()
    def __str__(self):
        return self.city_name

class Restaurants(models.Model):
    name = models.CharField(max_length=50, blank=False)
    address = models.CharField(max_length=50, blank=False)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    mob_no = models.CharField(max_length=10)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    website = models.URLField(blank=True)
    cover = models.ImageField(upload_to='restraunts/cover')

    def __str__(self):
        return self.name


# class ReviewRating(models.Model):
#     restraunt = models.ForeignKey(Restraunts, on_delete=models.CASCADE)
#     rating = models.DecimalField(max_digits=2, decimal_places=1)
#     review = models.TextField()
#     customer = models.ForeignKey(
#         Customers, on_delete=models.SET_NULL, null=True)





