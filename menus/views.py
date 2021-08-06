from orders.models import CartItem
from customers.models import Customers
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Category, MenuItem
from orders.models import Cart
from orders.views import get_session
from django.core.exceptions import ObjectDoesNotExist,PermissionDenied
from customers.models import Customers
from restaurants.models import Restaurants
from menus.models import Category
from django.http import JsonResponse
# Create your views here.

#home page 
def menus(request):
    if request.method == 'GET':
        menu_list = MenuItem.objects.all().order_by('-date_added')
        categories = list(Category.objects.all().values_list('name',flat=True))
        total_count =0
        try:
            if request.user.is_authenticated:
                cust= Customers.objects.get(user=request.user)
                total_count = Cart.objects.get(user=cust).count
                print(total_count)
        except [ObjectDoesNotExist,PermissionDenied]:
            print('permission denied ')
            pass
        request.session['categories'] = categories
        request.session['total_count'] = total_count
        context = {
            'menu_list': menu_list,
        }
        print(request.META.get('HTTP_REFERER'))
        return render(request, 'base/index.html', context)



def products(request):
    if request.method == 'GET':
        query = request.GET.get('category')
        user=Customers.objects.get(user=request.user)
        try:
            cartitem = list(CartItem.objects.filter(cart__user=user).values_list('id',flat=True))
        except ObjectDoesNotExist:
            pass

        products={
            'item':[],
            'is_added':[]
        }
      
        if query:
            menus = MenuItem.objects.filter(category__name=query).order_by('-date_added')
        else:
            menus = MenuItem.objects.all().order_by('-date_added')
            for item in menus:
                products['item'].append(item)
                if item.id in cartitem:
                    products['is_added'].append(True)
                else:
                     products['is_added'].append(False)
        print(products)
        restaurants = Restaurants.objects.all()
        categories= Category.objects.all()
        return render(request,'store/store.html',context={
        'product':menus,
        'restaurants':restaurants,
        'categories':categories
    })



def item(request,menu_id):
    if request.method == 'GET':
        obj = MenuItem.objects.get(id=menu_id)
        
        return render(request,'product/product-detail.html',{
            'menu':obj
        })





def cart(request):
    if request.method == 'GET':
        return render(request,'cart/cart.html')

        
def product_search(request):
    if request.method=='GET':
        
        query = request.GET.get('val')
        menuitems=list(MenuItem.objects.filter(item_name__icontains=query).values_list('item_name',flat=True))
        print(menuitems)

        return JsonResponse({'success':True,'data':menuitems},safe=False)