from django import forms
from django.forms import ModelForm
from users.models import User
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'date_of_birth')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1.lower() != password2.lower():
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class LoginForm(ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'password',) 

class RegisterForm(ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'date_of_birth', 'password1', 'password2',)
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1.lower() != password2.lower():
            raise forms.ValidationError("Passwords don't match")

        return cleaned_data


class ProfileForm(ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='First name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.CharField(label='Date of birth', widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(label='Phone number', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    country = forms.CharField(label='Country', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    city = forms.CharField(label='City', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    street = forms.CharField(label='Street', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    house_number = forms.CharField(label='House number', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    zip_code = forms.CharField(label='Zip code', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name','last_name', 'email', 'date_of_birth', 'phone_number', 'country', 'city','street', 'house_number', 'zip_code',) 

class NewUserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(NewUserPasswordChangeForm, self).__init__( *args, **kwargs)
    
    old_password = forms.CharField(label='Old password', strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'name': 'old_password'}))
    new_password1 = forms.CharField(label='New password', strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'name': 'new_password1'}))
    new_password2 = forms.CharField(label='Confirm password', strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'name': 'new_password2'}))

class NewUserPasswordResetEmailForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(NewUserPasswordResetEmailForm, self).__init__( *args, **kwargs)

    email = forms.CharField(label='Email', strip=False, widget=forms.EmailInput(attrs={'class': 'form-control', 'type': 'email', 'name': 'email'}))    


class NewUserPasswordResetForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(NewUserPasswordResetForm, self).__init__( *args, **kwargs)
    
    new_password1 = forms.CharField(label='New password', strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'name': 'new_password1'}))
    new_password2 = forms.CharField(label='Confirm password', strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'name': 'new_password2'}))
