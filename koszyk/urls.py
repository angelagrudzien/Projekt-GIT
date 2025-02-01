from django.urls import path
from .views import cart_view, add_to_cart, checkout


app_name = 'koszyk'

urlpatterns = [
    path("", cart_view, name="cart_view"),
    path("add/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path('checkout/', checkout, name='checkout'),
]