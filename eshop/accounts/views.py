from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from . import forms, models
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

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
            
            #activation https://medium.com/@frfahim/django-registration-with-confirmation-email-bb5da011e4ef
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
            return redirect('accounts/login/?command=verification&email='+email)
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
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are logged in")
            return redirect('index')
        else:
            messages.error(request, "Username or password is invalid.")
            return redirect('login')
    return render(request, 'login.html')

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