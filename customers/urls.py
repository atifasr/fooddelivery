from django.urls import path
from .views import *
app_name = 'customers'


urlpatterns = [
    path('register/',register,name='signup'),
    path('login_user/',login_user,name='login_user'),
    path('log_out/',log_out,name='log_out'),
    path('get_session/',get_session,name='get_session'),
]
