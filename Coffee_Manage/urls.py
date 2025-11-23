
from django.contrib import admin
from django.urls import path
from Coffee_Manage import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('menu/', views.menu_management, name='menu'),
    path('staff/', views.staff_management, name='staff'),
    path('customers/', views.customer_management, name='customers'),
    path('feedback/', views.feedback_management, name='feedback'),
    path('inventory/', views.inventory_management, name='inventory'),
    path('promotions/', views.promotions_management, name='promotions'),
]
