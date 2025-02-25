from django.urls import path
from . import views

urlpatterns = [
    path('profile', views.profile, name='profile'),
    path('login_users', views.login_user, name='login'),
]
