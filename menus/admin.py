from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from menus.models import Category, MenuItem, Ingredients
# Register your models here.


class CategoryAdmin(ModelAdmin):
    fields = ['name', 'description']
    list_display = ['name', 'description', 'uri_name']


class MenuItemAdmin(ModelAdmin):
    list_display = ('category', 'item_name', 'description', 'price')


class IngredientsAdmin(ModelAdmin):
    list_display = ('name', 'item',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
