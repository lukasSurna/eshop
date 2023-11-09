from django.shortcuts import render, get_object_or_404
from . import models

def index(request):
    products = models.Product.objects.all().filter(is_available=True)
    context = {
        'products': products,
    }
    return render(request, 'index.html', context)

def store(request, category_slug=None):
    categories = None
    products = None
    
    if category_slug != None:
        categories = get_object_or_404(models.Category, slug=category_slug)
        products = models.Product.objects.filter(category=categories, is_available=True)
        product_count = products.count()
    else:
        products = models.Product.objects.all().filter(is_available=True)
        product_count = products.count()
    
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store.html', context)