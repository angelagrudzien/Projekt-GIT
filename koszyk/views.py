from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from products.models import Product

from .models import Product, Cart, CartItem

from django.shortcuts import render
from .models import Cart

def cart_view(request):
    """Wyświetla zawartość koszyka"""
    cart, created = Cart.objects.get_or_create(user=request.user)  # Pobierz koszyk użytkownika

    return render(request, 'koszyk/koszyk.html', {'cart': cart})



def add_to_cart(request, product_id):
    """Dodaje produkt do koszyka"""
    product = get_object_or_404(Product, id=product_id)  # Znajdź produkt po id

    # Sprawdź, czy użytkownik ma już koszyk
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Jeśli produkt już znajduje się w koszyku, dodaj 1 do ilości, w przeciwnym razie utwórz nowy wpis w koszyku
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        # Jeśli produkt już jest w koszyku, zwiększ ilość
        cart_item.quantity += 1

    cart_item.save()  # Zapisz zmiany w bazie danych

    return JsonResponse({"message": "Produkt dodany do koszyka"})  # Można dodać odpowiedź w formacie JSON, jeśli używasz AJAX


def checkout(request):
    """Finalizuje zakup: zmniejsza stan magazynowy i czyści koszyk."""
    cart = get_object_or_404(Cart, user=request.user)
    for item in cart.items.all():
        if not item.product.decrease_stock(item.quantity):
            return JsonResponse({"error": f"Brak wystarczającej ilości {item.product.name}"}, status=400)

    cart.clear_cart()
    return JsonResponse({"message": "Zakup zakończony sukcesem"})