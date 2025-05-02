from django.urls import path
from . import views

urlpatterns = [
    path('', views.staff_profile, name='Staff Profile'),
    path('dashboard/', views.staff_dashboard, name='Dashboard'),
    path('order-detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order-detail/<int:order_id>/update-status/', views.update_order_status, name='update_order_status'),
    path('analytics/', views.staff_analytics, name='staff-analytics'),
    path('data/', views.staff_data_json, name='staff-data-json'),  
]
