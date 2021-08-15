
from django.db.utils import DatabaseError
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from customers.models import User,Customers
from restaurants.models import City
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction,IntegrityError
from orders.models import Cart
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse


# Create your views here.




@csrf_exempt
def register(request):
    city = City.objects.all()
    if request.method== 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        print(email)
        gender = request.POST.get('gender')
        city = request.POST.get('city')
        country = request.POST.get('country')
        print(country)
        password = request.POST.get('password')
        conf_password = request.POST.get('confirm_password')
        contact_no = request.POST.get('mob_number')
        print(conf_password,password)
        if password != conf_password:
            messages.add_message(request,messages.ERROR,'Password does not match kindly re-enter your password')
            return redirect('/register')
        else:
            try:
                with transaction.atomic(durable=True):
                    username = email.split('@')[0]
                    print(username)
                    user= User(username=username,first_name=first_name,last_name=last_name,email=email)  
                    user.set_password(password)  
                    user.save()       
                    city = City.objects.get(city_name=city)
                    customer=Customers(user=user,contact_no=contact_no,city=city,gender=gender)
                    customer.save()  
                    return redirect('/')     
            except IntegrityError:
                print('username already exists')
                messages.add_message(request,messages.ERROR,'Username already exists')
                return redirect('/register')
    return render(request,'register.html',{
        'city':city
    } )


    



@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        print(user)
        if user is not None:
            login(request,user)
            messages.add_message(request,messages.INFO,'successfully logged in!')
            return redirect('/')
        else:
            return redirect('/login_user/')

    return render(request, 'signin.html')




def log_out(request):
    if request.method == 'GET':
        logout(request)
        return redirect('/login_user/')