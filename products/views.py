from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product
from .forms import ProductForm

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def product_list_client(request):
    products = Product.objects.all()
    return render(request, 'products/product_list_client.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products:product_list')
    else:
        form = ProductForm()
    return render(request, 'products/product_create.html', {'form': form})

def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_list.html', {'form': form})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('products:product_list')



def increase_stock(request, pk):
    """Zwiększa ilość danego produktu w magazynie."""
    product = get_object_or_404(Product, pk=pk)
    product.increase_stock(1)

    return redirect('products:product_list')

def decrease_stock(request, pk):
    """Zmniejsza ilość danego produktu w magazynie, jeśli to możliwe."""
    product = get_object_or_404(Product, pk=pk)
    return redirect('products:product_list')


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))  

        if quantity > product.stock:  
            return redirect("products:product_detail", pk=product.id)

    return redirect("products:product_detail", pk=product.id)