from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    category_name = models.CharField(_("category name"), max_length=50, unique=True)
    slug = models.SlugField(_("slug"), max_length=100, unique=True)
    description = models.TextField(_("description"), max_length=255, blank=True)
    cat_image = models.ImageField(_("category image"), upload_to='photos/categories', blank=True)
    
    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return f'{self.category_name}'
    
    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"pk": self.pk})
