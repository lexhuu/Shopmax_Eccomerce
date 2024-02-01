from django import forms
from django.forms import ModelForm
from products.models import Order

class OrderForm(ModelForm):
    country_order = forms.CharField(label='Country', widget=forms.TextInput(attrs={'class': 'form-control'}))
    city_order = forms.CharField(label='City', widget=forms.TextInput(attrs={'class': 'form-control'}))
    street_order = forms.CharField(label='Street', widget=forms.TextInput(attrs={'class': 'form-control'}))
    house_number_order = forms.CharField(label='House number', widget=forms.TextInput(attrs={'class': 'form-control'}))
    zip_code_order = forms.CharField(label='Zip code', widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name_order = forms.CharField(label='First name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name_order = forms.CharField(label='Last name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email_order = forms.CharField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number_order = forms.CharField(label='Phone number', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Order
        fields = ('country_order', 'city_order', 'street_order', 'house_number_order', 'zip_code_order','first_name_order', 'last_name_order', 'email_order', 'phone_number_order',)
