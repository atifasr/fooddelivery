
# helper function for marking is_added_to cart option

def get_menu_list(menus,cartitem):
    menus_added = {}
    menu_items =[]
    # menus = MenuItem.objects.all().order_by('-date_added')
    for item in menus:
        menus_added['id'] = item.id
        menus_added['item_name'] = item.item_name
        menus_added['price'] = item.price
        menus_added['image_url'] = item.image_url
        if item.id in cartitem:
            
            menus_added['is_added']=True
        else:
            menus_added['is_added']=False
        menu_items.append(menus_added)
        menus_added = {}
    return menu_items