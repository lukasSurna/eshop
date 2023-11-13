from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')
        
        if not username:
            raise ValueError('User must have an username')
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
        
    class Meta:
        verbose_name = _("myAccountManager")
        verbose_name_plural = _("myAccountManagers")


    def get_absolute_url(self):
        return reverse("myAccountManager_detail", kwargs={"pk": self.pk})



class Account(AbstractBaseUser):
    first_name = models.CharField(_("first name"), max_length=50)
    last_name = models.CharField(_("last name"), max_length=50)
    username = models.CharField(_("username"), max_length=50, unique=True)
    email = models.EmailField(_("email"), max_length=100, unique=True)
    phone_number = models.CharField(_("phone"), max_length=50)
    
    date_joined = models.DateTimeField(_("date joined"), auto_now=False, auto_now_add=True)
    last_login = models.DateTimeField(_("last login"), auto_now=False, auto_now_add=True)
    is_admin = models.BooleanField(_("admin"), default=False)
    is_staff = models.BooleanField(_("staff"), default=False)
    is_active = models.BooleanField(_("active"), default=False)
    is_superadmin = models.BooleanField(_("superadmin"), default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    objects = MyAccountManager()
    
    class Meta:
        verbose_name = _("account")
        verbose_name_plural = _("accounts")

    def __str__(self):
        return f'{self.email}'
    
    def has_perm(self, perm, obj=None):
        return self.is_superadmin
    
    def has_module_perms(self, add_label):
        return True

    def get_absolute_url(self):
        return reverse("account_detail", kwargs={"pk": self.pk})


