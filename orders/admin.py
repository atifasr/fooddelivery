from django.contrib import admin
from .models import *
# Register your models here.

class PlacedOrderAdmin(admin.ModelAdmin):
    list_display = ['restraunt','order_time','estimated_delivery_time']


class CartItemAdmin(admin.ModelAdmin):
     list_display=('menu_item','cart','quantity')

    
class CartAdmin(admin.ModelAdmin):
    list_display=('user','session_id','count','total')





admin.site.register(PlacedOrder,PlacedOrderAdmin)
admin.site.register(Comment)
admin.site.register(Status)
admin.site.register(Cart,CartAdmin)
admin.site.register(CartItem,CartItemAdmin)
