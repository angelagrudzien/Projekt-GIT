from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Cart, CartItem


def cart_view(request):
    """Wyświetla zawartość koszyka."""
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, "koszyk/koszyk.html", {"cart": cart})


def add_to_cart(request, product_id):
    """Dodaje produkt do koszyka."""
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect("cart_view")  # Przekierowanie do widoku koszyka


def checkout(request):
    """Finalizuje zakup: zmniejsza stan magazynowy i czyści koszyk."""
    cart = get_object_or_404(Cart, user=request.user)

    for item in cart.items.all():
        if item.product.stock >= item.quantity:
            item.product.stock -= item.quantity
            item.product.save()
        else:
            return JsonResponse({"error": f"Brak wystarczającej ilości {item.product.name}"}, status=400)

    cart.clear_cart()
    return redirect("cart_view")  # Przekierowanie do pustego koszyka