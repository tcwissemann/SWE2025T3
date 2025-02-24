from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog, name='Shop'),
    path('product/<str:pk>/', views.product, name="Product_detail"),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('designs', views.view_designs)
]
