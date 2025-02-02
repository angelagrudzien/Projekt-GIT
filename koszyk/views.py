from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Product, Cart, CartItem, Order, OrderItem
from django.shortcuts import redirect
from django.shortcuts import render
from .models import Cart

def cart_view(request):
    """Wyświetla zawartość koszyka"""
    cart, created = Cart.objects.get_or_create(user=request.user)

    print(f"Koszyk użytkownika {request.user}: {cart}")  # Sprawdź, czy koszyk istnieje

    return render(request, 'koszyk/koszyk.html', {'cart': cart})


def add_to_cart(request, product_id):
    """Dodaje produkt do koszyka z uwzględnieniem dostępności w magazynie"""
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    try:
        quantity = int(request.POST.get("quantity", 1))
    except ValueError:
        return redirect("products:product_detail", product_id=product.id)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if created:
        cart_item.quantity = min(quantity, product.stock)  # Nie dodajemy więcej niż jest w magazynie
    else:
        cart_item.quantity = min(cart_item.quantity + quantity, product.stock)

    cart_item.save()
    return redirect("koszyk:cart_view")


def checkout(request):
    """Finalizuje zakup: zmniejsza stan magazynowy i czyści koszyk oraz zapisuje zamówienie"""
    cart = get_object_or_404(Cart, user=request.user)

    print(cart)  # Sprawdź, czy koszyk istnieje w terminalu

    if not cart.items.exists():
        return JsonResponse({"error": "Koszyk jest pusty"}, status=400)

    # Sprawdź dostępność produktów
    for item in cart.items.all():
        if item.quantity > item.product.stock:
            item.quantity = item.product.stock  # Ustaw ilość na maksymalną dostępną
            item.save()

    # Aktualizacja stanu magazynowego i opróżnienie koszyka
    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price  # Zapisz cenę w momencie zakupu
        )
        # Zmniejsz stan magazynowy
        item.product.stock -= item.quantity
        item.product.save()

    # Wyczyść koszyk
    cart.items.all().delete()
    return redirect("home")