from django.db import models
from category.models import Category
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class Product(models.Model):
    product_name = models.CharField(_("product name"), max_length=200, unique=True)
    slug = models.SlugField(_("slug"), max_length=250, unique=True)
    description = models.TextField(_("description"), max_length=500, blank=True)
    price = models.DecimalField(_("price"),max_digits=10 ,decimal_places=2)
    image = models.ImageField(_("image"), upload_to='photos/products')
    stock = models.IntegerField(_("stock"))
    is_available = models.BooleanField(_("is available"), default=True)
    category = models.ForeignKey(
        Category, 
        verbose_name=_("category"), 
        on_delete=models.CASCADE,
        related_name="products",
    )    
    created_date = models.DateTimeField(_("created date"), auto_now=False, auto_now_add=True)
    modified_date = models.DateTimeField(_("modified date"), auto_now=True, auto_now_add=False)
    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")

    def __str__(self):
        return f'{self.product_name}'

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk})

