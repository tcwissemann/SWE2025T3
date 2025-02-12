from django.contrib import admin
from .models import Product, ProductTemplate, ProductType, Design
# Register your models here.

admin.site.register([
    ProductType,
    Product,
    ProductTemplate,
    Design
])