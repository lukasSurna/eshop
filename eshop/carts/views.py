from django.shortcuts import render, redirect, get_object_or_404
from . import models
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.seesion.create()
    return cart

def add_cart(request, product_id):
    product = models.Product.objects.get(id=product_id)
    try:
        cart = models.Cart.objects.get(cart_id=_cart_id(request)) # get cart using _cart_id in sesssion
    except models.Cart.DoesNotExist:
        cart = models.Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()
    
    try:
        cart_item = models.CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except models.CartItem.DoesNotExist:
        cart_item = models.CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()
    return redirect('cart')

def remove_cart(request, product_id):
    cart = models.Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(models.Product, id=product_id)
    cart_item = models.CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_cart_item(request, product_id):
    cart = models.Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(models.Product, id=product_id)
    cart_item = models.CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')
    
def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = models.Cart.objects.get(cart_id=_cart_id(request))
        cart_items = models.CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (5 * total) / 100
        grand_total = total + tax
           
    except ObjectDoesNotExist:
        pass
    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }
    return render(request, 'cart.html', context)
