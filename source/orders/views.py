from django.shortcuts import render, redirect
from django.contrib import messages
from . import forms
import json
from .models import Order, OrderItem
from products.models import Product, Color, Size, Design

# Create your views here.
def cart(request):
    
    orderSent = False
    
    if request.method == "POST":
        order_dict = json.loads(request.POST['cart'])
        print(order_dict[0])
        
        #Create order object
        order = Order(user=request.user)
        order.save()
        
        #Create order items for order
        for order_item in order_dict:
            #get Product, Color, Size, Design, quantity
            item_product = Product.objects.get(sku=order_item['id'])
            item_color = Color.objects.get(id=int(order_item['color']))
            item_size = Size.objects.get(id=int(order_item['size']))
            item_design = Design.objects.get(id=int(order_item['design']))
            item_quantity = order_item['quantity']
            
            # create orderItem
            orderItem: OrderItem = OrderItem(\
                order=order,
                quantity=item_quantity,
                product=item_product,
                design=item_design,
                color=item_color,
                size=item_size
            )
            
            orderItem.save()
            
            order.subtotalCost += orderItem.product.price * orderItem.quantity
        
        # order.shippingCost = 
        order.taxCost = order.subtotalCost * 0.08
        order.totalCost = order.subtotalCost + order.taxCost + order.shippingCost
        
        order.save()
        
        orderSent = True
        
        messages.success(request, "Successful Order")
        
        return redirect('profile')

        
    cartForm = forms.cartForm()
    return render(request, "cart.html", {"cartForm": cartForm, 'orderSent': orderSent})
