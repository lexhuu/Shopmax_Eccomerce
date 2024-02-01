from django.contrib import admin
from products.models import Category, Product, Order, OrderProduct, Opinion


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'name', 'image', 'description',
                    'price', 'is_recommended', 'created_date_time', 'is_visible')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name_order', 'last_name_order', 'delivery_method_order', 'payment_method_order', 'country_order',
                    'city_order', 'street_order', 'house_number_order', 'zip_code_order', 'phone_number_order', 'email_order', 'date_time_order')


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'order_id')


class OpinionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'rating',
                    'content', 'created_date_time')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(Opinion, OpinionAdmin)
