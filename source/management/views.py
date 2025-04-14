from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from orders.models import Order, OrderItem, ORDER_STATUS_CHOICES
from .forms import ClaimOrderForm
from django.contrib import messages
from products.models import ProductImage
# Create your views here.

def isStaffCheck(user: User):
    return user.is_staff

def isAdminCheck(user: User):
    return user.is_staff and user.is_superuser

@user_passes_test(isAdminCheck)
def admin_profile(request):
    admin_user = request.user

    if request.method == 'POST' and 'cancel_order_id' in request.POST:
        order_id = int(request.POST['cancel_order_id'])
        order_to_cancel = Order.objects.get(id=order_id)
        order_to_cancel.claim = None
        order_to_cancel.save()

    recent_users = User.objects.order_by('-date_joined')[:3]
    active_employees = User.objects.filter(is_staff=True).order_by('-last_login')[:2]
    recent_orders_objects = Order.objects.order_by('-date')[:5]

    last_status_key = ORDER_STATUS_CHOICES[-1][0]
    claimed_orders_objects = Order.objects.filter(claim=admin_user).exclude(status=last_status_key)

    recent_orders = []
    for order in recent_orders_objects:
        order_info = {}
        order_info['number'] = f"#{order.id:06d}"
        order_info['id'] = order.id
        order_info['date'] = order.date.strftime('%d/%m/%Y - %H:%M%p')
        order_items = OrderItem.objects.filter(order=order)
        formatted_items = [item.product.name for item in order_items[:2]]
        if len(order_items) > 2:
            formatted_items.append("...")
        formatted_items = ", ".join(formatted_items)
        order_info['items'] = formatted_items
        recent_orders.append(order_info)

    claimed_orders = []
    for order in claimed_orders_objects:
        order_info = {}
        order_info['number'] = f"#{order.id:06d}"
        order_info['id'] = order.id
        order_info['date'] = order.date.strftime('%d/%m/%Y - %H:%M%p')
        order_items = OrderItem.objects.filter(order=order)
        formatted_items = [item.product.name for item in order_items[:2]]
        if len(order_items) > 2:
            formatted_items.append("...")
        formatted_items = ", ".join(formatted_items)
        order_info['items'] = formatted_items
        claimed_orders.append(order_info)

    context = {
        'user': admin_user,
        'recent_users': recent_users,
        'active_employees': active_employees,
        'recent_orders': recent_orders,
        'claimed_orders': claimed_orders,
    }

    return render(request, 'admin-profile.html', context)

@user_passes_test(isStaffCheck)
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
        formatted_items = [item.product.name for item in order_items[:2]]
        if len(order_items) > 2:
            formatted_items.append("...")
        formatted_items = ", ".join(formatted_items)
        order_info['items'] = formatted_items
        order_info['claimForm'] = ClaimOrderForm()
        orders.append(order_info)
        
    
    return render(request, 'staff-dashboard.html', {"orders":orders})

@user_passes_test(isStaffCheck)
def staff_profile(request):
    staff_user = request.user

    if request.method == 'POST' and 'cancel_order_id' in request.POST:
        order_id = int(request.POST['cancel_order_id'])
        order_to_cancel = Order.objects.get(id=order_id)
        order_to_cancel.claim = None
        order_to_cancel.save()

        return redirect('Staff Profile')

    last_status_key = ORDER_STATUS_CHOICES[-1][0]
    claimed_orders = Order.objects.filter(claim=staff_user).exclude(status=last_status_key)

    orders = []
    for order in claimed_orders:
        order_info = {
            'number': f"#{order.id:06d}",  # Format order number with leading zeros
            'id': order.id,
            'date': order.date.strftime('%d/%m/%Y - %H:%M%p'),  # Format the date
            'items': ", ".join(
                [item.product.name for item in OrderItem.objects.filter(order=order)[:2]] +
                (["..."] if OrderItem.objects.filter(order=order).count() > 2 else [])
            )
        }
        orders.append(order_info)

    # Fetch the 5 most recently placed orders
    recent_orders = Order.objects.all().order_by('-date')[:5]
    recent_orders_info = []

    for order in recent_orders:
        order_info = {
            'number': f"#{order.id:06d}",  # Format order number with leading zeros
            'id': order.id,
            'date': order.date.strftime('%d/%m/%Y - %H:%M%p'),  # Format the date
            'items': ", ".join(
                [item.product.name for item in OrderItem.objects.filter(order=order)[:2]] +
                (["..."] if OrderItem.objects.filter(order=order).count() > 2 else [])
            )
        }
        recent_orders_info.append(order_info)

    # Fetch the 3 most recent users if the logged-in user is a superuser
    recent_users = []
    if request.user.is_superuser:
        recent_users = User.objects.order_by('-date_joined')[:3]

    # Fetch the 2 most recently active employees (sorted by last login)
    active_employees = User.objects.filter(is_staff=True).order_by('-last_login')[:2]

    return render(request, 'staff-profile.html', {
        'user': staff_user,
        'orders': orders,
        'recent_users': recent_users,
        'active_employees': active_employees,
        'recent_orders': recent_orders_info,
    })

@user_passes_test(isStaffCheck)
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    
    order_items_data = []
    
    for item in order_items:
        item_info = {}
        
        item_info['product_name'] = item.product.name
        item_info['image'] = ProductImage.objects.get(product=item.product).imageURL
        item_info['designname'] = item.design.name
        item_info['designurl'] = item.design.image
        item_info['colorname'] = item.color.name
        item_info['sizename'] = item.size.name
        item_info['price'] = item.product.price / 100
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
        'order_summary': order_summary,
        "status_choices": ORDER_STATUS_CHOICES
    })
    
@user_passes_test(isStaffCheck)
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('order_status')
        
        if new_status in dict(ORDER_STATUS_CHOICES).keys():
            order.status = new_status
            order.save()
            messages.success(request, f"Order status updated to {dict(ORDER_STATUS_CHOICES)[new_status]}.")
        else:
            messages.error(request, "Invalid status.")
    
    return redirect('order_detail', order_id=order.id)
