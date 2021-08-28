from django.core.exceptions import AppRegistryNotReady, ObjectDoesNotExist
from customers.models import Customers
from django.contrib import messages
from .models import Cart,CartItem, OrderedItems,PlacedOrder
from django.shortcuts import redirect, render, resolve_url
from menus.models import MenuItem
import json
from collections import namedtuple
from .helpers import cartItems
import datetime
from random import randrange
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
# Create your views here.




def add_item(item):
    item.quantity +=1
    item.total_price += item.menu_item.price
    item.save()
    print(item.total_price)
    

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
        print(request.user)
        cust = Customers.objects.get(user = request.user)
        cart,created = Cart.objects.get_or_create(user=cust,defaults={
            'user':cust
        })
        menuitem = MenuItem.objects.get(id=menu_id)
        menuitem.is_added =True
        menuitem.save()

        item,item_created = CartItem.objects.get_or_create(menu_item=menuitem,cart=cart,defaults={
            'menu_item':menuitem,'quantity': 1,'total_price':menuitem.price,'cart':cart})
        
        # print(item)
        if not item_created:
            add_item(item)
        print(item)
        cart.count +=1
        cart.total = float(cart.total + int(item.menu_item.price))
        print(cart.total)
        cart.save()
    
    else:
        # get data from dictionary
        
        data = request.COOKIES.get('cartitem')
        print(data)
       

    return redirect('/view_cart')


def remove_cart(request,menu_id):
    if request.user.is_authenticated:
        cust=Customers.objects.get(user=request.user)
        cart = Cart.objects.get(user=cust)
        item = CartItem.objects.get(menu_item__id = menu_id,cart=cart)
        print(item)
        cart.count -= 1
        cart.total = float(cart.total - int(item.menu_item.price))
        cart.save()
        if item.quantity == 0:
            item.delete()
        else:
            decrease_item(item)
    else:
        data = request.COOKIES.get('cartitem')
        print(data)
       
        
    return redirect('/view_cart')


def view_cart(request):
    if request.method=='GET':
        total_value = 0
    
        if request.user.is_authenticated:
            try:
                customer = Customers.objects.get(user= request.user)
                cart=Cart.objects.get(user=customer)
                cartitem=CartItem.objects.filter(cart=cart)
                total_value = cart.total
                total_amount = float(total_value) * 0.85

            except ObjectDoesNotExist:
                messages.add_message(request,messages.INFO,'Cart is empty!')
                cartitem=None
        else:
            
            cartitem=cartItems(request)      

            print(cartitem)      
       
        return render(request,'cart/cart.html',{
            'cartitem':cartitem,
            'total_value':total_value,
            'total_amount':total_amount

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



#simple order id generation
def gen_orderid(quantity,zip_code,total_price):
    rand_range = randrange(1000)
    order_id = 'OD'+str(quantity)+str(zip_code)+str(rand_range)+str(int(total_price)) 
    return order_id
    


def place_order(request):
   
    total=0
    cust=None
    if request.user.is_authenticated:
        
        if request.method=="GET":

            try:
                cust = Customers.objects.get(user=request.user)
                cart = Cart.objects.get(user=cust)
                cartitems = CartItem.objects.filter(cart=cart)
                total = cart.total
                # print(cartitems)
                
            except Exception as e:
                print('exception-> ',e)

        if request.method== 'POST':
            cust = Customers.objects.get(user=request.user)
            cart = Cart.objects.get(user=cust)
            total = cart.total
            cartitems = CartItem.objects.filter(cart=cart)
            ordereditems = []
            ordered_item={}
            for item in cartitems:
                ordered_item['item_name']=item.menu_item.item_name
                ordered_item['quantity']=item.quantity
                ordered_item['total_price']=int(item.total_price)
                ordered_item['size']=item.size
                ordereditems.append(ordered_item)
                ordered_item={}


            #storing contact details
            contact={}
            contact["first_name"] = request.POST.get('first_name')
            contact["last_name"] = request.POST.get('last_name')
            contact["mob_no"] = request.POST.get('mob_no')
            contact["email"] = request.POST.get('email')
            print(contact)

            #storing delivery details
            delivery_info ={}
            delivery_info["city"] = request.POST.get('state')
            delivery_info["building"] = request.POST.get('building')
            delivery_info["zip_code"] = request.POST.get('zip_code')
            delivery_info["postal_code"] = request.POST.get('postal_code')
            delivery_info["street"] = request.POST.get('street')
         
            order_id = gen_orderid(ordereditems[0]['quantity'],delivery_info['zip_code'],ordereditems[0]['total_price'])

            # Saving details in session
            request.session['order']={
                'order_details':ordereditems,
                'contact_info':contact,
                'delivery_info':delivery_info,
                'cart_total':int(total)
            }
            return redirect('/checkout')
         
    else:
        cartitems = cartItems(request)        
            # return render(request,'checkout.html',{
            #     'ordered_item':ordered_item
            # })


    return render(request,'place-order.html',{
                'cartitems':cartitems,
                'total_amount':total,
                'customer':cust,
                
            })

client = razorpay.Client(auth=(settings.RAZOR_KEY, settings.RAZOR_SEC_KEY))


@csrf_exempt
def checkout(request):
    #process order 

    if request.method == 'POST':
        order_amount = 50000
        order_currency = 'INR'
        order_receipt = 'order_rcptid_11'
        notes = {'Shipping address': 'Bommanahalli, Bangalore'}   # OPTIONAL

        client.order.create(amount=order_amount, currency=order_currency, receipt=order_receipt, notes=notes)

        print('data submitted ')
  
    return render(request,'checkout.html')




def orders_placed(request):
    return render(request,'orders.html')