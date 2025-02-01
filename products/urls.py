from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

app_name = 'products'

urlpatterns = [
    path('', views.product_list_client, name='product_list_client'),
    path('produkty/<int:product_id>/dodaj/', views.add_to_cart, name='add_to_cart'),
    path('seller', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('create/', views.product_create, name='product_create'),
    path('edit/<int:pk>/', views.product_edit, name='product_edit'),
    path('delete/<int:pk>/', views.product_delete, name='product_delete'),
    path('increase_stock/<int:pk>/', views.increase_stock, name='increase_stock'),
    path('decrease_stock/<int:pk>/', views.decrease_stock, name='decrease_stock'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)