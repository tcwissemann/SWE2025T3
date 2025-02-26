from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

# Create your views here.
def profile(request):
    return render(request, 'profile.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Incorrect username or password, try again')
            return redirect('login')
    return render(request, 'authenticate/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('Purple Bubble')