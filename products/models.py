from django.db import models

# Create your models here.
# products/models.py
# from django.db import models
class Product(models.Model):
    name = models.CharField(max_length=255)  # Nazwa produktu    
    description = models.TextField()  # Opis produktu    
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Cena produktu    
    stock = models.IntegerField()  # Ilość w magazynie    
    image = models.ImageField(upload_to='products/', blank=True, null=True)  # Obrazek produktu    
    created_at = models.DateTimeField(auto_now_add=True)  # Data utworzenia produktu
    updated_at = models.DateTimeField(auto_now=True)  # Data ostatniej aktualizacji produktu
    
    def __str__(self):
        return self.name
 