import json

def cartItems(request):
    data = request.COOKIES.get('cartitem')
    data =json.loads(data)

    cartitem = []
    for val in data:
        data[val]['id']=val
        print(data[val])
    
    #creating dummmy representation
    for item in data:
        cart_item = {
            'id':data[item]['id'],
            'name':data[item]['name'],
            'total_price':data[item]['price'],
            'quantity':data[item]['quantity'],
            'price':data[item]['single_price'],
        }
        cartitem.append(cart_item)       
    return cartitem