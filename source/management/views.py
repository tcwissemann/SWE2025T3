from django.shortcuts import render
from orders.models import Order, OrderItem
from .forms import ClaimOrderForm
# Create your views here.

def staff_dashboard(request):
    
    if request.method == 'POST':
        claiming_staff_user = request.user
        order_id = int((request.POST['order_id']))
        
        claimed_order = Order.objects.get(id=order_id)
        claimed_order.claim = claiming_staff_user
        
        claimed_order.save()

    unclaimed_orders_objects = Order.objects.all().filter(claim__isnull=True).order_by('date')
    
    orders = []
    
    for order in unclaimed_orders_objects:
        order_info = {}
        order_info['number'] = f"#{order.id:06d}"
        order_info['id'] = order.id
        order_info['date'] = order.date.strftime('%d/%m/%Y - %H:%M%p')
        order_items = OrderItem.objects.filter(order=order)
        formatted_items = [item.product.product.name for item in order_items[:2]]
        if len(order_items) > 2:
            formatted_items.append("...")
        formatted_items = ", ".join(formatted_items)
        order_info['items'] = formatted_items
        order_info['claimForm'] = ClaimOrderForm()
        orders.append(order_info)
        
    
    return render(request, 'staff-dashboard.html', {"orders":orders})

def staff_profile(request):
    staff_user  = request.user
    claimed_orders = Order.objects.filter(claim=staff_user)
    orders = []
    
    for order in claimed_orders:
        order_info = {}
        order_info['number'] = f"#{order.id:06d}"
        order_info['id'] = order.id
        order_info['date'] = order.date.strftime('%d/%m/%Y - %H:%M%p')
        order_items = OrderItem.objects.filter(order=order)
        formatted_items = [item.product.product.name for item in order_items[:2]]
        if len(order_items) > 2:
            formatted_items.append("...")   
        formatted_items = ", ".join(formatted_items)
        order_info['items'] = formatted_items
        orders.append(order_info)
    
    return render(request, 'staff-profile.html', {'user':staff_user, 'orders':orders})