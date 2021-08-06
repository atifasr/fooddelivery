from django.core.exceptions import ObjectDoesNotExist
from customers.models import Customers
from django.contrib import messages
from .models import Cart,CartItem,PlacedOrder
from django.shortcuts import redirect, render, resolve_url
from menus.models import MenuItem
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
    

def remove_item(item):
    item.quantity -=1
    item.total_price -= item.menu_item.price
    item.save()
  



def add_cart(request,menu_id):
     #check if cart exists or not (id not then create)
    session_id = get_session(request)
    if request.user.is_authenticated:
        cust = Customers.objects.get(user= request.user)
        cart,created = Cart.objects.get_or_create(user=cust,defaults={
            'session_id':session_id,
            'user':cust
        })
    else:
        cart,created = Cart.objects.get_or_create(session_id=session_id,defaults={
            'session_id':session_id
        })
        

    menuitem = MenuItem.objects.get(id=menu_id)
    menuitem.is_added =True
    menuitem.save()
    item,item_created = CartItem.objects.get_or_create(menu_item=menuitem,cart=cart,defaults={
        'menu_item':menuitem,
        'quantity': 1,
        'total_price':menuitem.price,
        'cart':cart
    })
    cart.count+=1
    cart.total = float(cart.total) + float(item.quantity * item.menu_item.price)
    cart.save()
    if not item_created:
        add_item(item)
    

    return redirect('/view_cart')


def remove_cart(request,menu_id):
    session_id= get_session(request)
    cart = Cart.objects.get(session_id=session_id)
    item = CartItem.objects.get(menu_item__id = menu_id,cart=cart)
    cart.count-=1
    cart.total = float(cart.total) - float(item.quantity * item.menu_item.price)
    cart.save()
    if item.quantity == 0:
        item.delete()
    else:
        remove_item(item)
    
    return redirect('/view_cart')


def view_cart(request):
    if request.method=='GET':
        try:
            if request.user.is_authenticated:
                cust = Customers.objects.get(user= request.user)
                cart=Cart.objects.get(user=cust)

            else:
                cart=Cart.objects.get(session_id=get_session(request))
                print('calling from else')
            cartitem=CartItem.objects.filter(cart=cart)
            print(cartitem)
            total_value= cart.total
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
        cartitem=CartItem.objects.get(id=item_id)
        cust = Customers.objects.get(user= request.user)
        cart = Cart.objects.get(user=cust)
        cart.total -= cartitem.total_price
        cart.count -=cartitem.quantity
        cart.save()
        cartitem.delete()
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

