from django.shortcuts import render
from orders.models import Order, OrderItem
# Create your views here.

def dashboard(request):
    unclaimed_orders_objects = Order.objects.all().filter(claim__isnull=True).order_by('date')
    
    orders = []
    
    for order in unclaimed_orders_objects:
        order_info = {}
        order_info['number'] = f"#{order.id:06d}"
        order_info['id'] = order.id
        order_info['date'] = order.date.strftime('%d/%m/%Y - %H:%M%p')
        orders.append(order_info)
        
    
    return render(request, 'staff-dashboard.html', {"orders":orders})