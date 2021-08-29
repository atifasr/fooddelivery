from django.core.checks.messages import INFO
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
from django.contrib.sites.shortcuts import get_current_site
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
      
    
        if request.user.is_authenticated:
            try:
                customer = Customers.objects.get(user= request.user)
                cart=Cart.objects.get(user=customer)
                cartitem=CartItem.objects.filter(cart=cart)
                total_value = cart.total
                total_amount = round(float(total_value) * 0.85,2)

            except ObjectDoesNotExist:
                messages.add_message(request,messages.INFO,'Cart is empty!')
                cartitem = None
                total_amount = 0
                total_value = 0
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
    date = (datetime.datetime.now()).toordinal()
    order_id = 'OD'+str(quantity)+str(date)+str(zip_code)+str(rand_range)+str(int(total_price)) 
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
                ordered_item['id']=item.menu_item.id
                ordered_item['item_name']=item.menu_item.item_name
                ordered_item['quantity']=item.quantity
                ordered_item['total_price']=int(item.total_price)
                ordered_item['size']=item.size
                ordereditems.append(ordered_item)
                ordered_item={}

            print(ordered_item)

            #storing contact details
            contact={}
            contact["first_name"] = request.POST.get('first_name')
            contact["last_name"] = request.POST.get('last_name')
            contact["mob_no"] = request.POST.get('mob_no')
            contact["email"] = request.POST.get('email')
           

            #storing delivery details
            delivery_info ={}
            delivery_info["city"] = request.POST.get('state')
            delivery_info["building"] = request.POST.get('building')
            delivery_info["zip_code"] = request.POST.get('zip_code')
            delivery_info["postal_code"] = request.POST.get('postal_code')
            delivery_info["street"] = request.POST.get('street')
         
            # order_id = gen_orderid(ordereditems[0]['quantity'],delivery_info['zip_code'],ordereditems[0]['total_price'])

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
    if request.user.is_authenticated:
        #process order 
        zipcode= request.session['order']['delivery_info']['zip_code']
        quantity= request.session['order']['order_details'][0]['quantity']
        total_price = request.session['order']['cart_total']
        shipping_details = str(request.session['order']['delivery_info']['building'])+' '+request.session['order']['delivery_info']['city']+' '+str(request.session['order']['delivery_info']['zip_code'])
        

        order_id = gen_orderid(quantity,zipcode,total_price)

        call_back_url = 'http://'+str(get_current_site(request))+'/checkout/'

        print(total_price)
        order_amount = total_price   #converting to INR for Razor pay

        #Razor pay Config
        order_currency = 'INR'
        notes = {'Shipping address': shipping_details}   # OPTIONAL

        razor_order = client.order.create(dict(amount=order_amount, currency=order_currency, receipt='', notes=notes))
        print(razor_order)
        request.session['razor_pay_order_id'] = razor_order['id']
        
        context = {
            'call_back_url':call_back_url,
            'razor_pay_id':razor_order['id'],
        }

        #handle razor pay response
        if request.method == 'POST':
            zipcode= request.session['order']['delivery_info']['zip_code']
            quantity= request.session['order']['order_details'][0]['quantity']
            total_price = request.session['order']['cart_total']
            email = request.session['order']['contact_info']['email']
            mob_no = request.session['order']['contact_info']['mob_no']
            print('yes got the response')
            print(request.POST)


            razor_payment_id = request.POST.get('razorpay_payment_id','')
            
            razor_order_id = request.POST.get('razorpay_order_id','')
            print('razor order id',razor_order_id)
            payment_signature = request.POST.get('razorpay_signature','')

            order_id = gen_orderid(quantity,zipcode,total_price)
            customer = Customers.objects.get(user=request.user )
            order_placed = PlacedOrder(customer =customer ,order_id =order_id,total_price = total_price,city =request.session['order']['delivery_info']['city'],building = request.session['order']['delivery_info']['building'],zip_code= zipcode,razor_pay_order_id = razor_order_id,razor_pay_payment_id=razor_payment_id,razor_pay_signature = payment_signature,email=email,mob_no=mob_no)
            order_placed.save()
        
            

            # associated_items = OrderedItems()
            params_dict = {
                'razorpay_order_id': razor_order_id,
                'razorpay_payment_id': razor_payment_id,
                'razorpay_signature': payment_signature
            }
            cart_items = request.session['order']['order_details']
            print(cart_items)
        
            result = client.utility.verify_payment_signature(params_dict)
            if result == None:
                try:
                    placedorder = PlacedOrder.objects.get(razor_pay_payment_id=razor_payment_id)
                    print(placedorder)
                    placedorder.is_confirmed = True
                    placedorder.save()
                    cart_items = request.session['order']['order_details']
                    item_list = []
                    for item in cart_items:
                        menu = MenuItem.objects.get(id= item['id'])
                        inOrder = OrderedItems(ordereditem=placedorder,item=menu,item_name=item['item_name'],quantity=item['quantity'],total_price=item['total_price'],size=item['size'])
                        item_list.append(inOrder)
                    OrderedItems.objects.bulk_create(item_list)
                    #Cart cleared after payment
                    Cart.objects.filter(user=customer ).delete()
                    messages.add_message(request, messages.INFO, f'Congo your order for {order_id} order has been Placed!')
                except Exception as e:
                    pass
            return redirect('/orders_placed/')
    
    
        return render(request,'checkout.html',context)




def orders_placed(request):
    if request.method == 'GET':
        try:
            customer = Customers.objects.get(user=request.user)
            orders = PlacedOrder.objects.filter(customer=customer)
            ordered_items = OrderedItems.objects.filter(
                ordereditem__customer =customer
            )
            print(ordered_items)
        except ObjectDoesNotExist:
            orders = ordered_items = None
            messages.add_message(request,INFO,'Sorry! no orders yet ')
        context = {
            'orders':orders,
            'ordered_items':ordered_items
        }
        return render(request,'orders.html',context)