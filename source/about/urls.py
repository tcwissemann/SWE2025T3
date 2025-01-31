from django.urls import path
from . import views

urlpatterns = [
    path('', views.about_us, name='about'),
    path('gavin/', views.about_gavin, name='gavin'),
    path('jocelyn/', views.about_jocelyn, name='jocelyn'),
    path('swapnil/', views.about_swapnil, name='swapnil'),
    path('thomas/', views.about_thomas, name='thomas'),
]