from django.shortcuts import render
from orders.models import Order, OrderItem
# Create your views here.

def dashboard(request):
    unclaimed_orders = Order.objects.all().filter(claim__isnull=True)
    
    return render(request, 'staff-dashboard.html', {"orders": unclaimed_orders})