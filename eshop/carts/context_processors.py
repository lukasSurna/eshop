from . import models
from .views import _cart_id

#cart counter
def counter(request):
    
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = models.Cart.objects.filter(cart_id=_cart_id(request))
            if request.user.is_authenticated:
                cart_items = models.CartItem.objects.all().filter(user=request.user)
            else:
                cart_items = models.CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except models.Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)