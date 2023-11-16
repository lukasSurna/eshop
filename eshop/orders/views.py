from django.shortcuts import render, redirect
from carts.models import CartItem
from orders.models import Order
from . import forms
import datetime



def place_order(request, total=0, quantity=0):
    current_user = request.user
    
    #if cart is empty, redirect to store
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <=0:
        return redirect('store')
    
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    
    tax = (5 * total)/100
    grand_total = tax + total
    
    
    if request.method == 'POST':
        form = forms.OrderForm(request.POST)
        if form.is_valid():
            #store billing information inside Order table
            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_1 = form.cleaned_data['address_1']
            data.address_2 = form.cleaned_data['address_2']
            data.country = form.cleaned_data['country']
            data.zip_code = form.cleaned_data['zip_code']
            data.city = form.cleaned_data['city']
            data.order_comment = form.cleaned_data['order_comment']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR') #get user IP
            data.save() #save to get id
            #Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            mt = int(datetime.date.today().strftime('%m'))
            dt = int(datetime.date.today().strftime('%d'))
            date = datetime.date(yr,mt,dt)
            current_date = date.strftime('%Y%m%d')
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            return redirect('checkout')
    else:
         form = forms.OrderForm()
    return render(request, 'checkout.html', {'form': form})
            