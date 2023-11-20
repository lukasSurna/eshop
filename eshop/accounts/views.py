from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from . import forms, models
from accounts.models import UserProfile, Account
from orders.models import Order, OrderProduct
from carts import models
from carts.views import _cart_id
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
import requests

#user registration form
def register(request):
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            
            user = models.Account.objects.create_user(
                first_name = first_name, 
                last_name = last_name,  
                email = email, 
                password = password,
                username = username,
            )
            user.phone_number = phone_number
            user.save()
            
            #Create User Profile
            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = 'default/default-user.png'
            profile.save()
            
            #activation email https://medium.com/@frfahim/django-registration-with-confirmation-email-bb5da011e4ef
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            return redirect('/accounts/login/?command=verification&email='+email)
    else:           
        form = forms.RegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email=email, password=password)
        
        #Assign user to cart item
        if user is not None:
            try:
                cart = models.Cart.objects.get(cart_id=_cart_id(request))
                cart_item_exists = models.CartItem.objects.filter(cart=cart).exists()
                if cart_item_exists:
                    cart_item = models.CartItem.objects.filter(cart=cart)
                    for item in cart_item:
                        item.user = user
                        item.save()
            except:
                #if cart is empty
                pass 
            auth.login(request, user)
            messages.success(request, "You are logged in")
            #grab previous url. 
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                print("query...", query)
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    next_page = params['next']
                    return redirect(next_page)
                print('params ->', params)
            except:
                return redirect('dashboard')
        else:
            messages.error(request, "Username or password is invalid.")
            return redirect('login')
    return render(request, 'accounts/login.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, "You are logged out")
    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = models.Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, models.Account.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your Account is Activated!")
        return redirect('login')
    else:
        messages.error(request, "Invalid activation link")
        return redirect('register')
    
@login_required(login_url= 'login')
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id)
    orders_count = orders.count()
    #user profile pic from DB
    user_profile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'orders_count': orders_count,
        'user_profile': user_profile,
    }
    return render(request, 'accounts/dashboard.html', context)

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if models.Account.objects.filter(email=email).exists():
            user = models.Account.objects.get(email__exact=email)
            # Password Reset Email
            current_site = get_current_site(request)
            mail_subject = 'Password Reset'
            message = render_to_string('accounts/password_reset_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, 'Password reset email has been sent to your email')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exists!')
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')

def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = models.Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, models.Account.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please Reset Your Password')
        return redirect('password_reset')
    else:
        messages.error(request, 'The activation link has been expired')
        return redirect('login')
    
def password_reset(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            uid = request.session.get('uid')
            user = models.Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, "Password do not match")
            return render('password_reset')
    return render(request, 'accounts/password_reset.html')

@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders
    }
    return render(request, 'accounts/my_orders.html', context)

@login_required(login_url='login')
def edit_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = forms.UserForm(request.POST, instance=request.user)
        profile_form = forms.UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated")
            return redirect('edit_profile')
    else:
        user_form = forms.UserForm(instance=request.user)
        profile_form = forms.UserProfileForm(instance=user_profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_profile': user_profile,
    }
    
    return render (request, 'accounts/edit_profile.html', context)

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        
        user =Account.objects.get(username__exact=request.user.username)
        print(f'new_password: "{new_password}"')
        print(f'confirm_password: "{confirm_password}"')
        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password changed succesfully')
                return redirect('change_password')
            else:
                messages.error(request, 'PLease enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request, 'Password does not match')
            return redirect('change_password')
    return render(request, 'accounts/change_password.html')


def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    #Calculate subtotal
    subtotal = sum(order_product.product_price * order_product.quantity for order_product in order_detail)
    #Calculate grand total (including tax)
    grand_total = subtotal + order.tax

    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
        'grand_total': grand_total,
    }

    return render(request, 'accounts/order_detail.html', context)
