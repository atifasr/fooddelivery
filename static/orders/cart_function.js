
// var menu_id  = add_button.getAttribute('data-menu');


function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

CartItem = readCookie('cartitem')
CartItem=JSON.parse(CartItem)
console.log(CartItem)


console.log(user)
add_buttons = document.querySelectorAll('.add-button')
remove_buttons = document.querySelectorAll('.remove')
removeButtonCount = remove_buttons.length;

console.log('remove buttons ',remove_buttons.length);
buttonCount = add_buttons.length;

console.log(buttonCount)
for (let i =0; i< buttonCount;i++)
{
	add_buttons[i].addEventListener('click',function(e){

		menu_id = this.getAttribute('data-menu');
		action = this.getAttribute('data-action');
		console.log('added')
		console.log(this.getAttribute('data-name'));
		console.log(this.getAttribute('data-price'));
		console.log(menu_id)

		if (user == 'AnonymousUser'){

			if (action == 'add')
			{
				// if cart is not defined declare a empty cart
				if (CartItem == undefined)	CartItem = {}
				
				if (CartItem[menu_id] == undefined)
				{
					CartItem[menu_id] = {
						name : this.getAttribute('data-name'),
						quantity : 1 ,
						price: parseFloat(this.getAttribute('data-price')),
						single_price : parseFloat(this.getAttribute('data-price'))
					}	
				}
				else{
						console.log(' Inside ')
						CartItem[menu_id].quantity +=1;
						CartItem[menu_id].price += 	parseFloat(this.getAttribute('data-price'))
					}
				console.log(CartItem)	
			}
			else
			{
				if (CartItem[menu_id].quantity <= 0) {
					this.parentElement.parentElement.remove()
				}
				else{
					CartItem[menu_id].quantity -=1;
					CartItem[menu_id].price -= 	parseFloat(this.getAttribute('data-price'))
				}
			}
				
			}
			document.cookie = 'cartitem='+ JSON.stringify(CartItem)+';'+'path=/'
		
		}
		
	)

}


for (let i = 0; i< removeButtonCount ; i++){
	remove_buttons[i].addEventListener('click',function(e){
		e.preventDefault();
		id =this.getAttribute('data-menu');
		remove_item(this,id)
	})
}

let remove_item = function(item,menu_id){
	console.log(id)
	cartItem = JSON.parse(readCookie('cartitem')) 
	console.log(cartItem[menu_id])
	delete cartItem[menu_id]
	console.log(cartItem)
	document.cookie = 'cartitem='+ JSON.stringify(cartItem)+';'+'path=/'
	item.parentElement.parentElement.remove()
}

