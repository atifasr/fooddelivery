from django.contrib import admin
from .models import *
# Register your models here.

class PlacedOrderAdmin(admin.ModelAdmin):
    list_display = ['order_id','customer','order_time','estimated_delivery_time','is_confirmed','razor_pay_order_id','city','zip_code','email','mob_no','total_price']


class CartItemAdmin(admin.ModelAdmin):
     list_display=('menu_item','cart','quantity')

    
class CartAdmin(admin.ModelAdmin):
    list_display=('user','count','total')
    
class OrderedItemsAdmin(admin.ModelAdmin):
    list_display=('ordereditem','item','quantity','total_price','size')





admin.site.register(PlacedOrder,PlacedOrderAdmin)
admin.site.register(Comment)
admin.site.register(Status)
admin.site.register(Cart,CartAdmin)
admin.site.register(CartItem,CartItemAdmin)
admin.site.register(OrderedItems,OrderedItemsAdmin)
