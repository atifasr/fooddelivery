from django.core import paginator
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

from django.core.exceptions import ObjectDoesNotExist,PermissionDenied
from customers.models import Customers
from restaurants.models import Restaurants
from menus.models import Category
from django.http import JsonResponse
from django.core.paginator import Paginator
# Create your views here.

#home page 
def menus(request):
    if request.method == 'GET':
        menu_list = MenuItem.objects.all().order_by('-date_added')
        categories = list(Category.objects.all().values_list('name',flat=True))
        total_count = 0
        
        if request.user.is_authenticated:
            try:
                cust= Customers.objects.get(user=request.user)
                total_count = Cart.objects.get(user=cust).count
                print(total_count)
            except Exception as e:
                # print('permission denied ')
                print(f'cart for {request.user} is empty')
                print(e)
        request.session['categories'] = categories
        if request.user.is_authenticated:
            request.session['total_count'] = total_count
        else:
            from orders.helpers import cartItems
            _,_,total_count = cartItems(request)
            request.session['total_count'] = total_count

        context = {
            'menu_list': menu_list,
        }
        print(request.META.get('HTTP_REFERER'))
        return render(request, 'base/index.html', context)

from .helpers import get_menu_list

def products(request):
    if request.method == 'GET':
        query = request.GET.get('category')
        size = request.GET.get('size')
        # print(size)
        user=Customers.objects.get(user=request.user)
        try:
            cartitem = list(CartItem.objects.filter(cart__user=user).values_list('menu_item__id',flat=True))
        except ObjectDoesNotExist:
            pass
      
        if query:
            menus = MenuItem.objects.filter(category__name=query).order_by('-date_added')
            # helper function for marking added to cart 
            menu_items = get_menu_list(menus,cartitem)
            if size:
                menu_items = menu_items.filter(size=size)
        else:

            menus = MenuItem.objects.all().order_by('-date_added')
            # helper function for marking added to cart 
            menu_items = get_menu_list(menus,cartitem)
        
        paginate = Paginator(menu_items,9)
        page_objlist= page_num = None
        if request.GET.get('page'):
            page_num = request.GET.get('page')
            page_objlist = paginate.get_page(page_num)
        else:
            page_objlist = paginate.get_page(1)

        # print(len(page_objlist.object_list))
        

        restaurants = Restaurants.objects.all()
        categories= Category.objects.all()
        return render(request,'store/store.html',context={
        'product':page_objlist,
        'restaurants':restaurants,
        'categories':categories,
        'pages':paginate
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
        menuitems=list(MenuItem.objects.filter(item_name__icontains=query).values_list('id','item_name'))
        print(menuitems)

        return JsonResponse({'success':True,'data':menuitems},safe=False)