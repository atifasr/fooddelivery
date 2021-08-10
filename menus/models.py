
#----------------------------------------------------

from django.db import models
from django.template.defaultfilters import slugify
from customers.models import *
from django.http import request
from orders.models import CartItem
# Create your models here.---------------------------------


class Category(models.Model):
    name = models.CharField(max_length=25)
    uri_name = models.SlugField(max_length=25)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories')

    def save(self, *args, **kwargs):
        if not self.id:
            self.uri_name = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'


class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    recipe = models.TextField(blank=True)
    is_veg=models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=False)
    image = models.ImageField(upload_to='menu_items')
    date_added =models.DateTimeField(auto_now_add=True)
    restruant = models.ManyToManyField(to='restaurants.Restaurants',blank=True)
    offer = models.ManyToManyField(to='menus.Offer')
    # is_added= models.BooleanField(default=False)
    
    def __str__(self):
        return self.item_name
    
    @property
    def image_url(self):
        if self.image!= "":
            return self.image.url
        else:
            return " "
    # @property
    # def discounted_price(self):
    #     return self.price*self.offer.discount_percent


class Ingredients(models.Model):
    name = models.CharField(max_length=25)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)


# class ReviewRating(models.Model):
#     item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
#     rating = models.DecimalField(max_digits=2, decimal_places=1)
#     review = models.TextField()
#     customer = models.ForeignKey(
#         Customers, on_delete=models.SET_NULL, null=True)




class Offer(models.Model):
    name =  models.CharField(blank= True,max_length=50)
    discount = models.DecimalField(blank=True,max_digits=4,decimal_places=2)
    date_from = models.DateField()
    time_from =models.TimeField()
    date_to= models.DateField()
    time_to = models.TimeField()

    class Meta:
        ordering = ['id']

    @property
    def discount_percent(self):
        return (100-self.price)/100

    def __str__(self):
        return f'{self.name} offer'

    


