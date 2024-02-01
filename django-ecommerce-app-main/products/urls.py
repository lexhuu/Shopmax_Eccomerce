from django.urls import path
from products import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.product, name='product'),
    path('category/<int:pk>/', views.category_products, name='category_products'),
    path('search/', views.searched_products, name='search'),
    path('categories/', views.categories_all, name='categories_all'),
    path('cart/', views.cart, name='cart'),
    path('cart_action/<int:pk>/', views.cart_action, name='cart_action'),
    path('cart_quantity/<int:pk>/', views.cart_quantity, name='cart_quantity'),
    path('complete_order/', views.complete_order, name='complete_order'),
    path('opinion/<int:pk>/', views.opinion_action, name='opinion'),
    path('user_order/<int:pk>/', views.user_order, name='user_order'),
]
