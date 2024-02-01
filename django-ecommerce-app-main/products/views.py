from django.shortcuts import render, redirect
from products.models import Product, Category, OrderProduct, Order, Opinion
from django.db.models import Sum, F, Count, Avg
from products.forms import OrderForm
from django.core.paginator import Paginator
from django.core.mail import EmailMessage
from django.contrib import messages

def home(request):
    products = Product.objects.filter(is_visible=True, is_recommended=True).order_by('-id')
    context = {'products': products}
    return render(request, 'home.html', context=context)

def product(request, pk):
    product = Product.objects.get(pk=pk)
    opinions = Opinion.objects.filter(product=pk).order_by('-created_date_time')
    opinions_query = Opinion.objects.filter(product=pk).aggregate(Sum('rating'), Count('id'), Avg('rating'))
    opinions_rating = opinions_query['rating__sum']
    opinions_count = opinions_query['id__count']
    opinions_average_rating = opinions_query['rating__avg'] if opinions_count is not None and opinions_rating is not None else 0
    user_opinion = None

    if request.user.is_authenticated:
        try:
            user_opinion = Opinion.objects.get(user=request.user, product=pk)
        except Opinion.DoesNotExist:
            pass

    context = {
        'product': product,
        'opinions': opinions,
        'opinions_count': opinions_count,
        'opinions_rating': opinions_rating,
        'opinions_average_rating': opinions_average_rating,
        'user_opinion': user_opinion}
    
    return render(request, 'product.html', context=context)

def category_products(request, pk):
    products = Product.objects.filter(is_visible=True, category=pk).order_by('id')
    category = Category.objects.get(pk=pk)
    paginator = Paginator(products, 16)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'category': category}
    return render(request, 'category_products.html', context=context)

def searched_products(request):
    products = Product.objects.filter(is_visible=True, name__contains=request.POST['searched']).order_by('id')
    return render(request, 'searched_products.html', context={'products': products})

def categories_all(request):
    return render(request, 'categories_all.html')

def cart(request):
    if request.user.is_authenticated:
        initial_data = {}
        pk_cookie, products, cart_total = None, None, None    
        cookie = request.COOKIES.get('cart') or None

        if cookie:
            pk_cookie = [int(pk_order_product) for pk_order_product in cookie.split('_')]
            products = OrderProduct.objects.filter(pk__in=pk_cookie) 
            cart_total = OrderProduct.objects.filter(pk__in=pk_cookie).annotate(orderproduct_total=F('product__price') * F('quantity')).aggregate(total=Sum('orderproduct_total'))['total']

        context = {'products': products, 
                   'cart_total': cart_total, 
                   'form': OrderForm(initial=initial_data)} 

        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                order.user = request.user
                order.delivery_method_order = request.POST['delivery_method_order']
                order.payment_method_order = request.POST['payment_method_order']

                try:
                    OrderProduct.objects.filter(pk__in=pk_cookie).update(order_id=order.pk)
                    order.save()
                    
                    response = redirect('complete_order')
                    response.delete_cookie('cart')
                    email = EmailMessage('Your order is ready', f'Your order has been assigned a number #{order.pk}', to=[order.email_order])
                    email.send()
                    
                    return response
                except Exception as e:
                    messages.warning(request, f'Error processing the order: {e}')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.warning(request, f'Error in {field}: {error}')

        return render(request, 'cart.html', context=context)
    else:
        # If the user is not authenticated, redirect to the home page or login page.
        return redirect('home')  # You can change this to redirect to the login page if needed.

def cart_action(request, pk):
    response = redirect('cart')
    action = request.GET.get('action')
    cookie = request.COOKIES.get('cart') or None
    if action == 'add':
        product = Product.objects.get(pk=pk)
        if cookie:
            pk_cookie = [int(pk_order_product) for pk_order_product in cookie.split('_')]
            order_products = OrderProduct.objects.filter(pk__in=pk_cookie)
            found = any(item.product.pk==pk for item in order_products)
            if found:
                order_product = OrderProduct.objects.get(pk__in=pk_cookie, product=product)
                order_product.quantity += 1
                order_product.save() 
            else:
                new_product = OrderProduct.objects.create(product=product)
                response.set_cookie(key='cart', value=f'{cookie}_{new_product.pk}')
        else:
            new_product = OrderProduct.objects.create(product=product)
            response.set_cookie(key='cart', value=f'{new_product.pk}')
        return response

    elif action == 'remove':
        pk_cookie = [int(pk_order_product) for pk_order_product in cookie.split('_')]
        pk_cookie.remove(pk)
        if len(pk_cookie) > 0 :
            response.set_cookie(key='cart', value="_".join(map(str, pk_cookie)))
        else:
            response.delete_cookie('cart')
        order_product = OrderProduct.objects.get(pk=pk)
        order_product.delete()
    return response

def cart_quantity(request, pk):
    response = redirect('cart')
    order_product = OrderProduct.objects.get(pk=pk) 
    action = request.GET.get('action')
    if action == 'add':
        order_product.quantity += 1 

    elif action == 'remove':
        order_product.quantity -= 1

    if order_product.quantity == 0:
        cookie = request.COOKIES.get('cart') or None
        pk_cookie = [int(pk_order_product) for pk_order_product in cookie.split('_')]
        pk_cookie.remove(pk)

        if len(pk_cookie) > 0 :
            response.set_cookie(key='cart', value="_".join(map(str, pk_cookie)))
        else:
            response.delete_cookie('cart')
        order_product.delete()
    else:
        order_product.save()

    return response

def complete_order(request):
    return render(request, 'complete_order.html')

def opinion_action(request, pk):
    if request.user.is_authenticated:
        action = request.GET.get('action')
        if action == 'add':
            product = Product.objects.get(pk=pk)
            Opinion.objects.create(user=request.user, product=product, rating=request.POST['rating'], content=request.POST['content'])
        elif action == 'remove':
            opinion = Opinion.objects.get(user=request.user, product=pk)
            opinion.delete()
        return redirect('product', pk=pk)

def user_order(request, pk):
    order = Order.objects.get(pk=pk)
    if order.user == request.user:
            order_products = OrderProduct.objects.filter(order_id=order)
            cart_total = OrderProduct.objects.filter(order_id=order).annotate(orderproduct_total=F('product__price') * F('quantity')).aggregate(total=Sum('orderproduct_total'))['total']
            context = {
                'order': order,
                'order_products': order_products,
                'cart_total': cart_total
            }
            return render(request, 'user_order.html', context=context)
    else:
        return redirect('home')


