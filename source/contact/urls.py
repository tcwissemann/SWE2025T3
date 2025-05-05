from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.contact_us, name='user_contact'),
    path('messages/', views.admin_message_board, name='admin_messages'),
    path('messages/<int:message_id>/', views.admin_message_detail, name='admin_message_detail'),
    path('messages/<int:message_id>/delete/', views.admin_message_delete, name='admin_message_delete'),
]