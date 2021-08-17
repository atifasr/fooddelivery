from django.http import request
from django.urls import path
from .views import *
app_name = 'orders'


urlpatterns = [
    path('view_cart/',view_cart,name='view_cart'),
    path('add_cart/<menu_id>',add_cart,name='add_cart'),
    path('remove_cart/<menu_id>',remove_cart,name='remove_cart'),
    path('place_order/',place_order,name='place_order'),
    path('remove_item/<item_id>',remove_item,name='remove_item'),
    path('checkout/',checkout,name='checkout'),
    path('orders_placed/',orders_placed,name='orders_placed'),

]       
