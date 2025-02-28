from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeView

urlpatterns = [
    path('profile', views.profile, name='profile'),
    path('login_users', views.login_user, name='login'),
    path('logout_users', views.logout_user, name='logout'),
    path('register_users', views.register_user, name='register'),
    path('reset_password', views.reset_password, name='password_reset'),
]
