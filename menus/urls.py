from django.urls import path
from .views import *
app_name = 'menus'


urlpatterns = [
    path('', menus, name='menus'),
    path('products/', products, name='products'),
    path('item/<menu_id>', item, name='item'),
    path('product_search/', product_search, name='product_search'),
]
