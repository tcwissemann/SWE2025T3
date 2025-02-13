from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog, name='Shop'),
    path('product/', views.product, name="Product")
]