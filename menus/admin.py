from django.contrib import admin
from django.contrib.admin import ModelAdmin
from menus.models import Category, MenuItem, Ingredients,Offer
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'description']
    list_display = ['name', 'description', 'uri_name']


class MenuItemAdmin(ModelAdmin):
    list_display = ('category', 'item_name', 'description', 'price','get_restaurants')


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'item',)




admin.site.register(Offer)
admin.site.register(Category, CategoryAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Ingredients, IngredientsAdmin)

