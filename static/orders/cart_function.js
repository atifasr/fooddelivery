
let user = '{{request.user}}'
let add_button = document.querySelector('.add-button');
let menu_id  = add_button.getAttribute('data-menu');
let action  = add_button.getAttribute('data-action');

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
console.log(action)
console.log('{{menu.price}}')
add_button.addEventListener('click',function(e){
	console.log('added')
	if (user == 'AnonymousUser'){
	
		
		if (action == 'add')
		{
			// if cart is not defined declare a empty cart
			if (CartItem == undefined)	CartItem = {}
			
			if (CartItem[menu_id] == undefined)
			{
				CartItem[menu_id] = {
					name : '{{menu.item_name}}',
					quantity : 1 ,
					price: parseInt('{{menu.price}}')
				}	
			}
			else{

				CartItem[menu_id].quantity +=1;
				CartItem[menu_id].price += parseInt('{{menu.price}}')			
			}
				
			
			

			console.log(CartItem)	
		}
		else
		{
				
		}
			
		}
		document.cookie = 'cartitem='+ JSON.stringify(CartItem)+';'+'path=/'
	
	}
	
)

