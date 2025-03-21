from django.shortcuts import render, get_object_or_404, redirect
from orders.models import Order, OrderItem
from .forms import ClaimOrderForm
from django.contrib import messages
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
    staff_user = request.user

    if request.method == 'POST' and 'cancel_order_id' in request.POST:
        order_id = int(request.POST['cancel_order_id'])
        order_to_cancel = Order.objects.get(id=order_id)
        order_to_cancel.claim = None
        order_to_cancel.save()
        
        return redirect('Staff Profile')
    
    claimed_orders = Order.objects.filter(claim=staff_user).exclude(status='SH')
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
    
    return render(request, 'staff-profile.html', {'user': staff_user, 'orders': orders})

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    
    order_items_data = []
    
    for item in order_items:
        item_info = {}

        designed_product = item.product
        
        item_info['product_name'] = designed_product.product.name
        item_info['image'] = designed_product.product.imageURL
        item_info['designname'] = designed_product.design.name
        item_info['designurl'] = designed_product.design.image
        item_info['colorname'] = designed_product.color.name
        item_info['sizename'] = designed_product.size.name
        item_info['price'] = designed_product.product.price / 100
        item_info['quantity'] = item.quantity
        
        order_items_data.append(item_info)

    order_summary = {
        'subtotal': order.subtotalCost / 100,
        'tax': order.taxCost / 100,
        'shipping': order.shippingCost / 100,
        'total': order.totalCost / 100,
        'status': order.status
    }
    
    return render(request, 'staff-order-detail.html', {
        'order': order,
        'order_items': order_items_data,
        'order_summary': order_summary
    })

def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('order_status')

        status_messages = {
            'PL': 'Placed',
            'PR': 'Processing',
            'SH': 'Shipped',
        }
        
        if new_status in status_messages:
            order.status = new_status
            order.save()
            messages.success(request, f"Order status updated to {status_messages[new_status]}.")
        else:
            messages.error(request, "Invalid status.")
    
    return redirect('order_detail', order_id=order.id)
