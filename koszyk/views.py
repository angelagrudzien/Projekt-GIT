from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Product, Cart, CartItem
from django.shortcuts import redirect
from django.shortcuts import render
from .models import Cart

def cart_view(request):
    """Wyświetla zawartość koszyka"""
    cart, created = Cart.objects.get_or_create(user=request.user)  # Pobierz koszyk użytkownika

    return render(request, 'koszyk/koszyk.html', {'cart': cart})



def add_to_cart(request, product_id):
    """Dodaje produkt do koszyka z poprawnym pobieraniem ilości"""
    product = get_object_or_404(Product, id=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    try:
        quantity = int(request.POST.get("quantity", 1))  
    except ValueError:
        return redirect("products:product_detail", product_id=product.id)
    cart, _ = Cart.objects.get_or_create(user=request.user)


    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)


    if created:
        cart_item.quantity = quantity 
    else:
        cart_item.quantity += quantity

    cart_item.save()



    return redirect("koszyk:cart_view")


def checkout(request):
    """Finalizuje zakup: zmniejsza stan magazynowy i czyści koszyk"""
    cart = get_object_or_404(Cart, user=request.user)

    for item in cart.items.all():
        if item.quantity > item.product.stock:
 
            return redirect("koszyk:cart_view")

    for item in cart.items.all():
        item.product.stock -= item.quantity
        item.product.save()

    cart.items.all().delete()


    
    return redirect("home")