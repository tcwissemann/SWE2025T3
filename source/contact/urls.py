from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.user_contact, name='user_contact'),
    path('messages/', views.admin_message_board, name='admin_messages'),
    path('messages/<int:message_id>/', views.admin_message_detail, name='admin_message_detail'),
]