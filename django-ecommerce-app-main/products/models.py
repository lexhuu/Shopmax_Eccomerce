from django.db import models
from django.utils import timezone
from products.storage import OverriteFile
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# Define a custom validator for allowing only numeric values
numeric_validator = RegexValidator(
    regex='^[0-9]*$',
    message='Only numeric values are allowed.'
)

def numeric_validator(value):
    if not value.isdigit():
        raise ValidationError('Phone number must be numeric')
    elif len(value) != 10:
        raise ValidationError('Phone number must be 10 digits long')

class Category(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return str(self.name)
    
def get_image_filepath(self, filename):
    return f'./products/{self.name}_{self.created_date_time}.png'

def get_default_image():
    return f'./products/default.png'  

class Product(models.Model):
    category = models.ForeignKey("products.Category", on_delete=models.CASCADE, related_name='product_category', blank=False, null=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    image = models.ImageField(upload_to=get_image_filepath, default=get_default_image, storage=OverriteFile(), blank=False, null=False)
    description = models.CharField(max_length=1024, blank=True, null=True)
    price = models.FloatField(max_length=64, blank=False, null=False)
    is_recommended = models.BooleanField(default=True)
    created_date_time = models.DateTimeField(default=timezone.now, blank=False, null=False)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)
    
class Order(models.Model):

    DELIVERY_METHODS = [
        ((1, 'Courier delivery')),
        ((2, 'Pickup at a parcel locker')),
        ((3, 'Personal pickup')),
    ]

    PAYMENT_METHODS = [
        ((1, 'Cash/card payment on delivery')),
        ((2, 'Online payment by credit card')),
        ((3, 'Traditional money transfer')),
    ]

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='order_user', blank=True, null=True)
    first_name_order = models.CharField(max_length=255, blank=False, null=False)
    last_name_order = models.CharField(max_length=255, blank=False, null=False)
    delivery_method_order = models.IntegerField(choices=DELIVERY_METHODS, default=1, blank=False, null=False)
    payment_method_order = models.IntegerField(choices=PAYMENT_METHODS, default=1, blank=False, null=False)
    country_order = models.CharField(max_length=255, blank=False, null=False)
    city_order = models.CharField(max_length=255, blank=False, null=False)
    street_order = models.CharField(max_length=255, blank=False, null=False)
    house_number_order = models.CharField(max_length=255, blank=False, null=False)

    # Add the updated numeric_validator for zip_code_order and phone_number_order
    zip_code_order = models.CharField(max_length=255, validators=[numeric_validator], blank=False, null=False)

    # Update phone_number_validator to check length
    phone_number_order = models.CharField(max_length=255, validators=[lambda value: numeric_validator(value) and len(value) == 10], blank=False, null=False)

    # Add the built-in EmailValidator for email_order
    email_order = models.EmailField(max_length=255, validators=[EmailValidator()], blank=False, null=False)
    date_time_order = models.DateTimeField(default=timezone.now, blank=False, null=False)
     
    def clean(self):
        super().clean()

        # Custom validation for email, phone number, and zip code
        if not self.email_order:
            raise ValidationError(_('Email is required'), code='invalid')

        if not self.phone_number_order:
            raise ValidationError(_('Phone number is required'), code='invalid')

        if not self.zip_code_order:
            raise ValidationError(_('Zip code is required'), code='invalid')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id) 

class OrderProduct(models.Model):
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name='orderproduct_product', blank=False, null=False)
    quantity = models.FloatField(default=1.0, blank=False, null=False)
    order_id = models.ForeignKey("products.Order", on_delete=models.CASCADE, related_name='orderproduct_order_id', blank=True, null=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    def __str__(self):
        return str(self.id)
    
class Opinion(models.Model):
    product =  models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name='opinion_product', blank=False, null=False)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='opinion_user', blank=False, null=False)
    rating = models.CharField(max_length=1, blank=False, null=False, default='5')
    content = models.CharField(max_length=1024, blank=True, null=True)
    created_date_time = models.DateTimeField(default=timezone.now, blank=False, null=False)

    class Meta:
        unique_together = ('product', 'user')


    def __str__(self):
        return str(self.id)
    
    
