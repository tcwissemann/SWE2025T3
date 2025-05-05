from io import BytesIO
import json
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Product, Size, Color, Design, ProductImage, ProductPreview, ProductColor
from . import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
import django.contrib.auth.models
import threading
from PIL import Image, ImageOps, ImageChops

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

    products = Product.objects.filter(is_available=True)

    if category != 'all':
        products = products.filter(category=category)

    if min_price:
        products = products.filter(price__gte=int(min_price) * 100)
    if max_price:
        products = products.filter(price__lte=int(max_price) * 100)

    context = {
        'products': [
            {
                "get_absolute_url": product.get_absolute_url(),
                "imageURL": ProductImage.objects.get(product=product).image.url,
                "name": product.name,
                "price_in_dollars": product.price_in_dollars()
            } for product in products
        ]
    }
    
    print(context)
    return render(request, 'catalog.html', context)

def product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    sizes = Size.objects.filter(productType=product)
    colors = Color.objects.all()
    productImage = ProductImage.objects.get(product=product)
    
    userDesignsContext = getUserDesignsContext(request)
    designs = userDesignsContext[1] if userDesignsContext != None else None
    
    return render(request, "product-detail.html", {
        'product': product,
        'sizes': sizes,
        'colors': colors,
        'designs': designs,
        'productImage': {
            'imageURL': productImage.image.url,
            'top': productImage.start_y,
            'left': productImage.start_x,
            'width': productImage.end_x - productImage.start_x,
            'height': productImage.end_y - productImage.start_y
        },
        'previews': getPreviews(request.user, product)
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

def mergeImages(background: Image.Image, overlay: Image.Image, mask: Image.Image, start: tuple[int, int], end: tuple[int, int])->Image.Image:
    overlay_width = end[0] - start[0]
    overlay_height = end[1] - start[1]
    
    # pads the design to fit in printable box
    resized_overlay = ImageOps.pad(overlay, (overlay_width, overlay_height), color=(255,255,255,0))
    
    # multiplies by background mask twice for extra texture
    multiplied_overlay = ImageChops.multiply(resized_overlay, mask)
    multiplied_overlay = ImageChops.multiply(multiplied_overlay, mask)
    
    # creates new image
    new_img = Image.new('RGBA', background.size)

    # pastes product image
    new_img.paste(background)
    
    # pastes
    new_img.paste(multiplied_overlay, (start[0], start[1], end[0], end[1]), resized_overlay)
    
    return new_img

def create_previews(design: Design):
    designImage = Image.open(design.image).convert('RGBA')
    for product in ProductImage.objects.all():
        textureMask = Image.open(product.texture_mask).convert('RGBA')
        
        for color in Color.objects.all():
            productPreview = ProductColor.objects.filter(productImage=product, color=color).last()
            productPreviewImage = Image.open(productPreview.image).convert('RGBA')
            print(f"making {design.name} for {product.product.name} in color {color.name}")

            start_pos = (int(productPreviewImage.size[0] * product.start_x/100), int(productPreviewImage.size[1] * product.start_y/100))
            end_pos = (int(productPreviewImage.size[0] * product.end_x/100), int(productPreviewImage.size[1] * product.end_y/100))

            mergedImage = mergeImages(productPreviewImage, designImage,  textureMask, start_pos, end_pos)
            
            # mergedImage.show()
            
            django_image_io = BytesIO()
            
            mergedImage.convert('RGB').save(django_image_io, format='JPEG', optimize=True, quality=50)
            
            djangoImageFile = File(django_image_io, f'{design.name}_{product.product.name}_{color.name}.jpg')
            
            newPreview = ProductPreview(product=product, design=design, color=color, image=djangoImageFile)
            
            newPreview.save()
        
@login_required()
def designs(request):
    userDesignsContext: tuple[User, list[Design]] = getUserDesignsContext(request)
    if userDesignsContext == None:
        return render(request, 'designs.html', {"isLoggedIn": False})
        
    if request.method == 'POST':
        print(request.FILES)
        print(request.POST)
        image_file = request.FILES['image']
        print(type(image_file))
        name = request.POST['name']
        if settings.USE_S3:
            upload = Design(user=userDesignsContext[0], name=name, image=image_file)
            upload.save()
            
            background_job = threading.Thread(target=create_previews, args=[upload])
            background_job.start()
    
    form = forms.DesignForm()
    return render(request, 'designs.html', {"isLoggedIn": True, 'form': form, 'designs': userDesignsContext[1]})

def test_request(request):
    data = json.loads(request.body)
    obj = {
        'text': f'this is a server response for user {request.user} with parameters {data}'
    }
    
    print(f"{data= }")
    
    print(f'ajax received from {request.user.username}')
    
    response = HttpResponse(json.dumps(obj), 'application/json', charset='utf-8')
    return response

# returns json with previews
def getPreviews(user: django.contrib.auth.models.User, product: Product)->str:
    previews = {}
    productImage = ProductImage.objects.filter(product=product).last()
    print(user)
    for design in Design.objects.filter(user=user):
        design_previews = {}
        for color in Color.objects.all():
            try:
                preview = ProductPreview.objects.filter(color=color, design=design, product=productImage).last()
                if preview.image.url:
                    # design_previews[color.id] = preview.image.url
                    design_previews.update({color.id: preview.image.url})
                else:
                    # design_previews[color.id] = 'null'
                    design_previews.update({color.id: 'null'})
            except ProductPreview.DoesNotExist:
                design_previews.update({color.id: 'null'})
        # previews[design.id] = design_previews
        previews.update({design.id: design_previews})
    print(previews)
    return json.dumps(previews)
    