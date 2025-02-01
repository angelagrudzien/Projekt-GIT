from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list_client, name='product_list_client'),
    path('seller', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('create/', views.product_create, name='product_create'),
    path('edit/<int:pk>/', views.product_edit, name='product_edit'),
    path('delete/<int:pk>/', views.product_delete, name='product_delete'),
    path('increase_stock/<int:pk>/', views.increase_stock, name='increase_stock'),
    path('decrease_stock/<int:pk>/', views.decrease_stock, name='decrease_stock'),
]