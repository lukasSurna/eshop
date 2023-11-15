from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from shop.models import Product
from accounts.models import Account


class Cart(models.Model):
    cart_id = models.CharField(_("cart id"), max_length=250)
    date_added = models.DateField(_("date added"), auto_now=False, auto_now_add=True)
    

    class Meta:
        verbose_name = _("cart")
        verbose_name_plural = _("carts")

    def __str__(self):
        return f'{self.cart_id}'

    def get_absolute_url(self):
        return reverse("cart_detail", kwargs={"pk": self.pk})


class CartItem(models.Model):
    user = models.ForeignKey(
        Account, 
        verbose_name=_("user"), 
        on_delete=models.CASCADE,
        null = True,
    )
    product = models.ForeignKey(
        Product, 
        verbose_name=_("product"), 
        on_delete=models.CASCADE,
        related_name='products'
    )
    cart = models.ForeignKey(
        Cart, 
        verbose_name=_("cart"), 
        on_delete=models.CASCADE,
        related_name='carts',
        null = True,
    )
    quantity = models.IntegerField(_("quantity"))
    is_active = models.BooleanField(_("is active"), default=True)


    class Meta:
        verbose_name = _("cartItem")
        verbose_name_plural = _("cartItems")
        
    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.product}'

    def get_absolute_url(self):
        return reverse("cartItem_detail", kwargs={"pk": self.pk})

