from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from .models import ContactMessage
from .forms import ContactForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ContactForm
from django.contrib import messages

def isStaffCheck(user: User):
    return user.is_staff

def isAdminCheck(user: User):
    return user.is_staff and user.is_superuser

@login_required
@user_passes_test(isAdminCheck)
def admin_message_board(request):
    messages = ContactMessage.objects.all().order_by('-created_at') # Order by newest first
    return render(request, 'admin-message-board.html', {'messages': messages})

def contact_us(request):
    pass

def contact_thank_you(request):
    pass

@login_required
def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save(commit=False)
            contact_message.user = request.user
            contact_message.name = f"{request.user.first_name} {request.user.last_name}"
            contact_message.save()
            messages.success(request, 'Your message has been submitted. We will get back to you soon.')
            return redirect('/users/profile') # Replace with your success URL
    else:
        form = ContactForm()
    return render(request, 'contact-us.html', {'form': form})

@login_required
@user_passes_test(isAdminCheck)
def admin_message_detail(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)
    return render(request, 'admin-message-detail.html', {'message': message})

@login_required
@user_passes_test(isAdminCheck)
def admin_message_delete(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)
    if request.method == 'POST':
        message.delete()
        messages.success(request, f"Message from {message.user.username if message.user else 'Guest'} deleted successfully.")
        return redirect('admin-message-board')
    return render(request, 'admin-message-delete-confirm.html', {'message': message})

@login_required
@user_passes_test(isAdminCheck)
def admin_message_delete(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)
    message.delete()
    messages.success(request, f"Message from {message.user.username if message.user else 'Guest'} deleted successfully.")
    return redirect('admin_messages') # Redirect back to the message board