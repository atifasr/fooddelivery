from django.core.exceptions import ObjectDoesNotExist
from customers.models import Customers
from django.contrib import messages
from .models import Cart,CartItem,PlacedOrder
from django.shortcuts import redirect, render, resolve_url
from menus.models import MenuItem
import json
# Create your views here.

#helper function for session retreival
def get_session(request):
    if request.session.session_key:
        return request.session.session_key
    else:
        request.session.save()
        return request.session.session_key
        




def add_item(item):
    item.quantity +=1
    item.total_price += item.menu_item.price
    item.save()
    

def decrease_item(item):
    item.quantity -=1
    item.total_price -= item.menu_item.price
    item.save()
  


# add to cart in database for logged in users 
# and just make a dict for unauthenticated users 

def add_cart(request,menu_id):
    # add cart for logged in user
     #check if cart exists or not (id not then create)
    if request.user.is_authenticated:
        cust = Customers.objects.get(user= request.user)
        cart,created = Cart.objects.get_or_create(user=cust,defaults={
            'user':cust
        })
        menuitem = MenuItem.objects.get(id=menu_id)
        menuitem.is_added =True
        menuitem.save()
        
        item,item_created = CartItem.objects.get_or_create(menu_item=menuitem,cart=cart,defaults={
            'menu_item':menuitem,'quantity': 1,'total_price':menuitem.price,'cart':cart})
        cart.count+=1
        cart.total = float(cart.total) + float(item.quantity * item.menu_item.price)
        cart.save()
        print(item)
        if not item_created:
            add_item(item)
    
    else:
        # get data from dictionary
        data = request.COOKIES.get('cart')
        print(data)
        cart = {
            'user':'',
            'count':'',
            'total':'',
            'updated':'',
            'timestamp':''
            }

    return redirect('/view_cart')


def remove_cart(request,menu_id):
    if request.user.is_authenticated:
        cust=Customers.objects.get(user=request.user)
        cart = Cart.objects.get(user=cust)
        item = CartItem.objects.get(menu_item__id = menu_id,cart=cart)
        print(item)
        cart.count-=1
        cart.total = float(cart.total) - float(item.quantity * item.menu_item.price)
        cart.save()
        if item.quantity == 0:
            item.delete()
        else:
            decrease_item(item)
        
    return redirect('/view_cart')


def view_cart(request):
    if request.method=='GET':
        try:
            if request.user.is_authenticated:
                cust = Customers.objects.get(user= request.user)
                cart=Cart.objects.get(user=cust)
                cartitem=CartItem.objects.filter(cart=cart)
                total_value= cart.total
            else:
                cartitem = {}
                total_value = 0
                data = request.COOKIES.get('cart')
                print(data)
                #get data from cookies as user is not logged in
                # cart=Cart.objects.get(session_id=get_session(request))
            
        except ObjectDoesNotExist:
            messages.add_message(request,messages.INFO,'Cart is empty!')
            total_value = 0
            cartitem=None
        return render(request,'cart/cart.html',{
            'cartitem':cartitem,
            'total_value':total_value

        })






def remove_item(request,item_id):
    if request.method == 'GET':
        if request.user.is_authenticated:
            cartitem=CartItem.objects.get(id=item_id)
            cust = Customers.objects.get(user= request.user)
            cart = Cart.objects.get(user=cust)
            cart.total -= cartitem.total_price
            cart.count -=cartitem.quantity
            cart.save()
            cartitem.delete()
        else:
            #is user is not logged in
            pass
        return redirect('/view_cart')



def place_order(request):
    if request.method=='GET':
        if request.user.is_authenticated:
            try:
                cust = Customers.objects.get(user=request.user)
                cart = Cart.objects.get(user=cust)
                cartitems = CartItem.objects.filter(cart=cart)
            except ObjectDoesNotExist:
                print('objects not found ')
        else:
            return redirect('/register')

    
        return render(request,'place-order.html',{
            'cartitems':cartitems,
            'total_amount':cart.total,
            'customer':cust,
        })
    

    if request.method == 'POST':
        pass

