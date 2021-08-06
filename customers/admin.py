from django.contrib import admin
from .models import *


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    fields = ['username', 'date_of_birth', 'email']
    list_display = ('username', 'date_of_birth', 'email')

class CustomersAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact_no', 'gender','time_joined')



admin.site.register(Customers,CustomersAdmin)
admin.site.register(User,UserAdmin)
