from django.contrib import admin
from users.models import User
from users.forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'date_of_birth', 'phone_number',  'country',
                    'city', 'street', 'house_number', 'zip_code', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'first_name', 'last_name', 'email', 'date_of_birth', 'phone_number', 'country',
                    'city', 'street', 'house_number', 'zip_code', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined')
                }
        ),)
    add_fieldsets = (
        (None, {
            'fields': ('username', 'first_name', 'last_name', 'email', 'date_of_birth', 'password1', 'password2',  'is_staff', 'is_active', 'is_superuser',)
            }
        ),)

admin.site.register(User, UserAdmin)
