from django.shortcuts import render
from products.models import Product

# Create your views here.
def about_us(request):
    featured_product = Product.objects.first()
    if featured_product:
        featured_product_price = featured_product.price_in_dollars()
    else:
        featured_product_price = None
    return render(request, "main-page.html", {"featured_product": featured_product, "featured_product_price": featured_product_price})
