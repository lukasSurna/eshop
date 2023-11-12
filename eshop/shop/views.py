from django.shortcuts import render, get_object_or_404
from . import models
from carts.models import CartItem
from carts.views import _cart_id


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

def product_detail(request, category_slug, product_slug):
    try:
        single_product = models.Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()     
    except Exception as e:
        raise e
    
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
    return render(request, 'product_detail.html', context)