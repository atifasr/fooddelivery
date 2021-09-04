import json



# get cart from cookies 
def cartItems(request):
    data = request.COOKIES.get('cartitem')
    print('Cookie data ',data)
    data =json.loads(data)
    print(data)
    cartitem = []
    for val in data:
        data[val]['id']=val
        # print(data[val])
    
    #creating dummmy representation of cart items
    total_value = 0
    total_quantity = 0
    for item in data:
        cart_item = {
            'id':data[item]['id'],
            'name':data[item]['name'],
            'total_price':data[item]['price'],
            'quantity':data[item]['quantity'],
            'price':data[item]['single_price'],
        }
        total_value += data[item]['price']
        total_quantity += data[item]['quantity']
        cartitem.append(cart_item)       
    return cartitem,total_value,total_quantity