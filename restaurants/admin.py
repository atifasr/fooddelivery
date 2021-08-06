from django.contrib import admin
from .models import Restaurants,City
# Register your models here.


class RestrauntsAdmin(admin.ModelAdmin):
    list_display =  ['name','address','mob_no']


class CityAdmin(admin.ModelAdmin):
    fields = ['city_name','zip_code']
    list_display= ('city_name','zip_code')

admin.site.register(Restaurants,RestrauntsAdmin)
admin.site.register(City,CityAdmin)
