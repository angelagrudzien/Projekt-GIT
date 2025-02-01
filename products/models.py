from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)  # Liczba dostępnych produktów
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def decrease_stock(self, amount=1):
        """Zmniejsza stan magazynowy o podaną ilość."""
        if self.stock >= amount:
            self.stock -= amount
            self.save()
            return True  # Udało się zmniejszyć stan magazynowy
        return False  # Brak wystarczającej ilości produktów

    def increase_stock(self, amount=1):
        """Zwiększa stan magazynowy o podaną ilość."""
        self.stock += amount
        self.save()