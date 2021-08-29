from os import truncate
from django.db import models
from django.db.models.aggregates import Max
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
# from restaurants.models import Restraunts
from customers.models import Customers

#----------------------------

# Create your models Here.
class PlacedOrder(models.Model):
    customer = models.ForeignKey(Customers,on_delete=models.CASCADE)
    order_id= models.CharField(max_length=255)
    order_time = models.DateTimeField(
        auto_now_add=True)
    estimated_delivery_time = models.TimeField(blank=True,null=True)
    actual_delivery_time = models.TimeField(blank=True,null=True)
    #total price of order
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    is_delivered = models.BooleanField(default=False)
    is_confirmed  = models.BooleanField(blank=True,null=True)
    city = models.CharField(max_length=25)
    building = models.CharField(max_length=25,blank=True)
    zip_code = models.CharField(max_length=25)
    razor_pay_order_id =models.CharField(max_length=255,null=True,blank=True) 
    razor_pay_payment_id =models.CharField(max_length=255,null=True,blank=True) 
    razor_pay_signature =models.CharField(max_length=255,null=True,blank=True) 
    email = models.CharField(max_length=25,null=False,blank=False)
    mob_no = models.CharField(max_length=20,blank=False,null=True)

   


# Customers Comment while placing the order
class Comment(models.Model):
    text = models.TextField()
    created = models.DateTimeField()
    is_req = models.BooleanField()
    is_complaint = models.BooleanField()
    order = models.ForeignKey(PlacedOrder, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)




# order status
class Status(models.Model):
    status = models.CharField(max_length=25)
    order = models.ManyToManyField(PlacedOrder)
    time = models.TimeField(auto_now=True)

#---------------------------------



class Cart(models.Model):
    user = models.ForeignKey(Customers, null=True, blank=True, on_delete=models.CASCADE)
    #total items
    count = models.PositiveIntegerField(default=0)
    #total amount
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "User: {} has {} items in their cart. Their total is ${}".format(self.user, self.count, self.total)



#items related to placed order
class OrderedItems(models.Model):
    ordereditem = models.ForeignKey(PlacedOrder,on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(to='menus.MenuItem',on_delete=models.SET_NULL,null=True)
    item_name = models.CharField(max_length=255,blank=False,null=False)
    quantity = models.PositiveIntegerField(null=True)
    total_price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    size = models.CharField(max_length=25,blank=True)

    def __str__(self):
        return f'{self.item.item_name}'
        


class CartItem(models.Model):
    menu_item = models.ForeignKey(to='menus.MenuItem', null=True, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, null=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(null=True)
    total_price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    size = models.CharField(max_length=25)
    

    def __str__(self):
        return "This entry contains {} {}(s).".format(self.quantity, self.menu_item)

        