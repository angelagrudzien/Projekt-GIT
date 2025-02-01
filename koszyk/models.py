from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.conf import settings
from products.models import Product
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

class Cart(models.Model):
       # user = "elo"
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def total_price(self):
        """Zwraca całkowitą wartość koszyka."""
        return sum(item.total_price() for item in self.items.all())

    def clear_cart(self):
        """Czyści koszyk po zakupie."""
        self.items.all().delete()

    def __str__(self):
        return f"Koszyk {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        """Zwraca cenę dla danej pozycji w koszyku."""
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"



def add_to_cart(request, product_id):
    """Dodaje produkt do koszyka."""
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return JsonResponse({"message": "Produkt dodany do koszyka"})


def checkout(request):
    """Finalizuje zakup: zmniejsza stan magazynowy i czyści koszyk."""
    cart = get_object_or_404(Cart, user=request.user)
    for item in cart.items.all():
        if not item.product.decrease_stock(item.quantity):
            return JsonResponse({"error": f"Brak wystarczającej ilości {item.product.name}"}, status=400)

    cart.clear_cart()
    return JsonResponse({"message": "Zakup zakończony sukcesem"})


