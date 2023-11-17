from django.contrib import admin
from . import models

class OrderProductInline(admin.TabularInline):
    model = models.OrderProduct
    extra = 0
    readonly_fields = ('user', 'product', 'quantity', 'product_price', 'ordered')

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'email', 'order_total', 'status']
    list_filter = ['status']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    list_per_page = 20
    inlines = [OrderProductInline]
    
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderProduct)
