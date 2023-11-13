from django.shortcuts import render
from . import forms, models

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
    else:           
        form = forms.RegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)

def login(request):
    return render(request, 'accounts/login.html')

def logout(request):
    return
