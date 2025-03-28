from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Product, Size, Color, Design
from . import forms
from django.conf import settings
from django.contrib.auth.models import User
from mainpage.views import about_us
import django.contrib.auth.models

def getUserDesignsContext(request)->tuple[User, list[Design]] | None:
    try:
        USER = User.objects.get(id=request.user.id)
    except django.contrib.auth.models.User.DoesNotExist as e:
        return None
    else:
        # return USER, Design.objects.all().filter(user=USER)
        return USER, Design.objects.all().filter(user=USER)

def catalog(request):
    category = request.GET.get('category', 'all')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.all()

    if category != 'all':
        products = products.filter(category=category)

    if min_price:
        products = products.filter(price__gte=int(min_price) * 100)
    if max_price:
        products = products.filter(price__lte=int(max_price) * 100)

    context = {'products': products}
    return render(request, 'catalog.html', context)

def product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    sizes = Size.objects.filter(productType=product)
    colors = Color.objects.all()
    
    userDesignsContext = getUserDesignsContext(request)
    designs = userDesignsContext[1] if userDesignsContext != None else None
    
    return render(request, "product-detail.html", {
        'product': product,
        'sizes': sizes,
        'colors': colors,
        'designs': designs
    })

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

@login_required()
def designs(request):
    userDesignsContext: tuple[User, list[Design]] = getUserDesignsContext(request)
    if userDesignsContext == None:
        return render(request, 'designs.html', {"isLoggedIn": False})
        
    if request.method == 'POST':
        print(request.FILES)
        print(request.POST)
        image_file = request.FILES['image']
        name = request.POST['name']
        if settings.USE_S3:
            upload = Design(user=userDesignsContext[0], name=name, image=image_file)
            upload.save()
    
    form = forms.DesignForm()
    return render(request, 'designs.html', {"isLoggedIn": True, 'form': form, 'designs': userDesignsContext[1]})

from django.shortcuts import render
from .models import Product  # Replace with your actual app name
