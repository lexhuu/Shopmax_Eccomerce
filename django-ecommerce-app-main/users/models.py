from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.core.validators import validate_email

class UserManager(BaseUserManager):
    def create_user(self, username, email, password, first_name, last_name, date_of_birth, **extra_fields):
        user = self.model(username=username, email=email, first_name=first_name, last_name=last_name, date_of_birth=date_of_birth, **extra_fields)
        validate_email(email)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, email, password, **extra_fields):
        superuser = self.model(username=username, email=email, **extra_fields)
        validate_email(email)
        superuser.set_password(password)
        superuser.first_name = 'Admin'
        superuser.last_name = 'Admin'      
        superuser.date_of_birth = '2000-01-01'  
        superuser.is_staff = True      
        superuser.is_active = True                     
        superuser.is_superuser = True    
        superuser.save()
        return superuser


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(max_length=255, unique=True, blank=False, null=False)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=False, null=False)
    country = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    house_number = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(default=timezone.now, blank=False, null=False)
    date_joined = models.DateTimeField(default=timezone.now, blank=False, null=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    def __str__(self):
        return str(self.username)