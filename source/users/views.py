from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from orders.models import Order, OrderItem
from .forms import RegisterUserForm

# Create your views here.
@login_required()
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-date')
    
    for order in orders:
        order.order_number = f"#{str(order.id).zfill(6)}"

        order_items = OrderItem.objects.filter(order=order)
        formatted_items = [item.product.name for item in order_items[:2]]
        if len(order_items) > 2:
            formatted_items.append("...")
        order.formatted_items = ", ".join(formatted_items)
        order.display_total = order.totalCost / 100
        order.status_display = order.get_status_display()

    return render(request, "profile.html", {"orders": orders})


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('Staff Profile')
            else:
                return redirect('profile')
        else:
            messages.error(request, 'Incorrect username or password, try again')
            return redirect('login')
    return render(request, 'authenticate/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('Purple Bubble')

def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            messages.success(request, f'Account created for {username}')
            return redirect('Purple Bubble')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = RegisterUserForm()
    return render(request, 'authenticate/register.html', {'form': form})

def reset_password(request):
    return render(request, 'authenticate/reset-password.html')
