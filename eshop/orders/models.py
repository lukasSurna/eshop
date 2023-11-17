from django.db import models
from accounts.models import Account
from shop.models import Product
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    STATUS = (
        (0, 'New'),
        (1, 'Accepted'),
        (2, 'Completed'),
        (3, 'Cancelled'),
    )
    
    user = models.ForeignKey(
        Account, 
        verbose_name=_("user"), 
        on_delete=models.SET_NULL,
        null=True,
    )
    order_number = models.CharField(_("order_number"), max_length=20)
    first_name = models.CharField(_("first name"), max_length=50)
    last_name = models.CharField(_("last name"), max_length=50)
    phone = models.CharField(_("phone"), max_length=20)
    email = models.CharField(_("email"), max_length=50)
    address_1 = models.CharField(_("address 1"), max_length=50)
    address_2 = models.CharField(_("address 2"), max_length=50, blank=True)
    country = models.CharField(_("country"), max_length=50)
    city = models.CharField(_("city"), max_length=50)
    zip_code = models.CharField(_("zip code"), max_length=15, default=0)
    order_comment = models.CharField(_("order comment"), max_length=250)
    order_total = models.FloatField(_("order total"))
    tax = models.FloatField(_("tax"))
    status = models.PositiveIntegerField(_("status"), choices=STATUS, default=0)
    ip = models.CharField(_("ip"), max_length=25, blank=True)
    is_ordered = models.BooleanField(_("is ordered"), default=False)
    created_at = models.DateTimeField(_("created at"), auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True, auto_now_add=False)
    
    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")

    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def full_address(self):
        return f'{self.address_1} {self.address_2}'
    
    def __str__(self):
        return f"{self.first_name}"

    def get_absolute_url(self):
        return reverse("order_detail", kwargs={"pk": self.pk})


class OrderProduct(models.Model):
    order = models.ForeignKey(
        Order, 
        verbose_name=_("order"), 
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        Account, 
        verbose_name=_("user"), 
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product, 
        verbose_name=_("product"), 
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField(_("quantity"))
    product_price = models.FloatField(_("product price"))
    ordered = models.BooleanField(_("ordered"), default=False)
    created_at = models.DateTimeField(_("created at"), auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True, auto_now_add=False)
    
    
    class Meta:
        verbose_name = _("orderProduct")
        verbose_name_plural = _("orderProducts")

    def __str__(self):
        return f"{self.product.product_name}"

    def get_absolute_url(self):
        return reverse("orderProduct_detail", kwargs={"pk": self.pk})
