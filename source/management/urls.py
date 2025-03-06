from django.urls import path
from . import views

urlpatterns = [
    path('', views.staff_profile, name='Staff Profile'),
    path('claim-orders/', views.staff_dashboard, name='Unclaimed Orders')
]