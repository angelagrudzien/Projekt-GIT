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
    """Dodaje produkt do koszyka"""
    product = get_object_or_404(Product, id=product_id)

    # Sprawdź, czy użytkownik ma już koszyk
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Jeśli produkt już znajduje się w koszyku, dodaj 1 do ilości, w przeciwnym razie utwórz nowy wpis w koszyku
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        # Jeśli produkt już jest w koszyku, zwiększ ilość
        cart_item.quantity += 1

    cart_item.save()  # Zapisz zmiany w bazie danych

    # Zwróć komunikat jako odpowiedź JSON
    return JsonResponse({"message": "Produkt został dodany do koszyka!"})


def checkout(request):
    """Finalizuje zakup: zmniejsza stan magazynowy i czyści koszyk."""
    cart = get_object_or_404(Cart, user=request.user)
    for item in cart.items.all():
        if not item.product.decrease_stock(item.quantity):
            return JsonResponse({"error": f"Brak wystarczającej ilości {item.product.name}"}, status=400)

    cart.clear_cart()
    return JsonResponse({"message": "Zakup zakończony sukcesem"})


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

    def get_items_list(self):
        """Zwraca listę zakupionych produktów w formie stringa"""
        return ", ".join([f"{item.quantity}x {item.product.name}" for item in self.items.all()])

    def __str__(self):
        return f"Zamówienie {self.id} - {self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')} - {self.get_items_list()}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Cena w momencie zakupu

    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product.name} - {self.price} PLN"

