from django import forms
from . import models

class OrderForm(forms.ModelForm):
    order_comment = forms.CharField(widget=forms.Textarea, required=False)
    class Meta:
        model = models.Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_1', 'address_2', 'country', 'zip_code', 'city', 'order_comment']
