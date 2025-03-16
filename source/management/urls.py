from django.urls import path
from . import views

urlpatterns = [
    path('', views.staff_profile, name='Staff Profile'),
    path('claim-orders/', views.staff_dashboard, name='Unclaimed Orders'),
    path('order-detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order-detail/<int:order_id>/update-status/', views.update_order_status, name='update_order_status'),
]
