"""
URL configuration for source project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from products.views import designs
from orders.views import cart

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', include('about.urls')),
    path('', include('mainpage.urls')),
    path('shop/', include('products.urls')),
    path('order/', include('orders.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('users/', include('users.urls')),
    path('designs/', designs),
    path('cart/', cart),
    path('dashboard', include('management.adminUrls')),
    path('staff/', include('management.urls')),
    path('', include('contact.urls'))
]
