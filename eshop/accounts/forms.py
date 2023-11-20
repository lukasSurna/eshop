from django import forms
from . import models

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
     'placeholder': 'Enter password',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
     'placeholder': 'Confirm password'   
    }))
    
    class Meta:
        model = models.Account
        fields = ['first_name', 'last_name', 'username','phone_number', 'email', 'password']
        
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )
        
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter Username'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Your E-mail'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
    
class UserForm(forms.ModelForm):
    class Meta:
        model = models.Account
        fields = ('first_name', 'last_name', 'phone_number')
        
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        
class UserProfileForm(forms.ModelForm):
    #Remove current picture field in form
    profile_picture = forms.ImageField(required=False, error_messages={'Invalid':("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = models.UserProfile
        fields = ('address_1', 'address_2', 'city', 'zip_code', 'country', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'