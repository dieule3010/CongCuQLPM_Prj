
from django.contrib import admin
from django.urls import path
from Coffee_Manage import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('staff-delete/', views.staff_delete, name='staff_delete'),
    path('staff-add/', views.staff_add, name='staff_add'),
    path('menu-add/', views.menu_add, name='menu_add'),
    path('menu-delete/', views.menu_delete, name='menu_delete'),
    path('feedback_reply/', views.feedback_reply, name='feedback_reply'),
    path('feedback_delete/', views.feedback_delete, name='feedback_delete'),
    path('revenue/', views.report_revenue, name='report_revenue'),
]
