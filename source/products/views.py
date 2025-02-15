from django.http import HttpResponse
import json
from django.shortcuts import render

# Create your views here.
def catalog(request):
    return render(request, "catalog.html")

def product(request):
    return render(request, "product-detail.html")

# general logic for when dynamic product page is implemented
def add_to_cart(request, item_id):
    if request.method == 'POST':
        cart = request.COOKIES.get('cart', '[]')
        cart = json.loads(cart)

        if not isinstance(cart, dict):
            cart = {}


        if str(item_id) in cart:
            cart[str(item_id)]['quantity'] += 1
        else:
            item = Item.objects.get(id=item_id)
            cart[str(item_id)] = {
                'quantity': 1,
                'name': item.name,
                'price': str(item.price)
            }

        response = HttpResponse('Added to cart')
        response.set_cookie('cart', json.dumps(cart), max_age=604800) # 1 week

        return response

def view_cart(request):
    cart = request.COOKIES.get('cart', '[]')
    cart_items = json.loads(cart)

    items = Item.objects.filter(id__in=cart_items)

    return render(request, 'cart.html', {'items': items})

def clear_cart(request):
    response = HttpResponse('Cart cleared')
    response.delete_cookie('cart')
    return response

def remove_from_cart(request, item_id):
    cart = json.loads(request.COOKIES.get('cart', '{}'))
    if str(item_id) in cart:
        del cart[str(item_id)]

    response = HttpResponse('Item removed')
    response.set_cookie('cart', json.dumps(cart), max_age=604800)
    return response

def update_quantity(request, item_id):
    quantity = int(request.POST.get('quantity', 1))
    cart = json.loads(request.COOKIES.get('cart', '{}'))
    
    if str(item_id) in cart:
        if quantity > 0:
            cart[str(item_id)]['quantity'] = quantity
        else:
            del cart[str(item_id)]

    response = HttpResponse('Quantity updated')
    response.set_cookie('cart', json.dumps(cart), max_age=604800)
    return response