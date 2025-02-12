from django.contrib import admin
from .models import Order, OrderItem, CartItem
# Register your models here.

admin.site.register([
    Order,
    OrderItem,
    CartItem,
])