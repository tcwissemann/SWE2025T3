from django.shortcuts import render
from products.models import Product, ProductImage

# Create your views here.
def about_us(request):
    featured_product = Product.objects.filter(is_available=True).first()

    if featured_product:
        featured_product_price = featured_product.price_in_dollars()
        featured_product_image = ProductImage.objects.get(product=featured_product).image.url
    else:
        featured_product_price = None
        featured_product_image = None

    return render(request, "main-page.html", {
        "featured_product": featured_product,
        "featured_product_price": featured_product_price,
        "featured_product_image": featured_product_image
    })
