from django.shortcuts import render, redirect
from django.urls import reverse
from carts.models import CartItem
from orders.models import Order, OrderProduct
from shop.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from . import forms
import datetime

def order_complete(request, order_id):
    order = Order.objects.get(pk=order_id)
    order_products = OrderProduct.objects.filter(order=order)
    subtotal = sum(order_product.product_price for order_product in order_products)
    subtotal + order.tax,
    context = {
        'order': order,
        'order_products': order_products,
        'subtotal': subtotal,
        'tax': order.tax,
        'grand_total': subtotal + order.tax,
    }
    return render(request, 'order_complete.html', context)

def place_order(request, total=0, quantity=0):
    current_user = request.user
    
    # if cart is empty, redirect to store
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    tax = (5 * total) / 100
    grand_total = tax + total
    
    # Order instance
    data = Order()
    data.user = request.user
    data.order_total = grand_total
    data.tax = tax
    data.ip = request.META.get('REMOTE_ADDR')  # get user IP
    data.save()  # save to get id

    # Generate order number
    yr = int(datetime.date.today().strftime('%Y'))
    mt = int(datetime.date.today().strftime('%m'))
    dt = int(datetime.date.today().strftime('%d'))
    date = datetime.date(yr, mt, dt)
    current_date = date.strftime('%Y%m%d')
    order_number = current_date + str(data.id)
    data.order_number = order_number
    data.save()

    if request.method == 'POST':
        form = forms.OrderForm(request.POST)
        if form.is_valid():
            # Store billing information inside Order table
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
            data.save()  # save to update order information

            # CartItems to OrderProducts table
            for cart_item in cart_items:
                order_product = OrderProduct()
                order_product.order = data
                order_product.user= request.user
                order_product.product_id = cart_item.product_id
                order_product.quantity = cart_item.quantity
                order_product.product_price = cart_item.product.price
                order_product.ordered = True
                order_product.save()
                
                # Reduce qty of product
                product = Product.objects.get(id=cart_item.product_id)
                product.stock -= cart_item.quantity
                product.save()
            
            # Clear Cart
            CartItem.objects.filter(user=request.user).delete()
            
            # Order received Email
            mail_subject = 'Confirmation of Your Recent Order'
            message = render_to_string('order_received_email.html', {
                'user': request.user,
                'order': data,
            })
            to_email = request.user.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            
            # Use reverse to get the URL of the order_complete view
            return redirect(reverse('order_complete', args=[data.id]))
    else:
        form = forms.OrderForm()
    return render(request, 'checkout.html', {'form': form})
