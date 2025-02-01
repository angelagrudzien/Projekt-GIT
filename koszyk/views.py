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



from django.contrib import messages
from django.shortcuts import redirect

def add_to_cart(request, product_id):
    """Dodaje produkt do koszyka"""
    product = get_object_or_404(Product, id=product_id)

    # Sprawdź, czy użytkownik ma już koszyk
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Odczytaj ilość produktu z formularza
    quantity = int(request.POST.get('quantity', 1))  # domyślnie 1, jeśli nie podano

    # Sprawdzamy, czy produkt już jest w koszyku
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        # Jeśli produkt już jest w koszyku, zwiększ ilość
        cart_item.quantity += quantity

    cart_item.save()  # Zapisz zmiany w bazie danych

    # Dodaj komunikat do wiadomości
    messages.success(request, f'Produkt "{product.name}" został dodany do koszyka.')

    # Zwróć użytkownika na stronę produktu (czyli nie przekierowujemy do koszyka)
    return render(request, 'products/product_detail.html', {'product': product})

def checkout(request):
    """Finalizuje zakup: zmniejsza stan magazynowy i czyści koszyk."""
    cart = get_object_or_404(Cart, user=request.user)
    for item in cart.items.all():
        if not item.product.decrease_stock(item.quantity):
            return JsonResponse({"error": f"Brak wystarczającej ilości {item.product.name}"}, status=400)

    cart.clear_cart()
    return JsonResponse({"message": "Zakup zakończony sukcesem"})