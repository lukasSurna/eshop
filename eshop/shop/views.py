from django.shortcuts import render
from . import models

def index(request):
    products = models.Product.objects.all().filter(is_available=True)
    context = {
        'products': products,
    }
    return render(request, 'index.html', context)
