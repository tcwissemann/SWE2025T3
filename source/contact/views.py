from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage
from .forms import ContactForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test

def isStaffCheck(user: User):
    return user.is_staff

def isAdminCheck(user: User):
    return user.is_staff and user.is_superuser
@login_required

def user_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            message = form.cleaned_data['message']
            ContactMessage.objects.create(
                user=request.user,
                title=title,
                message=message,
            )
            messages.success(request, 'Your message has been submitted. We will get back to you as soon as possible.')
            # a notification to admins here
            return redirect('user_dashboard') # Redirect to the user's dashboard or a thank you page
    else:
        form = ContactForm()
    return render(request, 'contact-us.html', {'form': form})


@login_required
@user_passes_test(isAdminCheck)
def admin_message_board(request):
    messages = ContactMessage.objects.all().order_by('-created_at') # Order by newest first
    return render(request, 'admin-message-board.html', {'messages': messages})

@login_required
@user_passes_test(isAdminCheck)
def admin_message_detail(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)
    return render(request, 'admin-message-detail.html', {'message': message})