from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from users.forms import LoginForm, RegisterForm, ProfileForm
from products.models import Order
from django.core.paginator import Paginator

def login_user(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html', {'form': LoginForm})

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Additional logic if needed
            return redirect('login')
        else:
            # If the form is not valid, render the registration form with errors
            return render(request, 'register.html', {'form': form})

    # If the request method is not POST, render the registration form
    return render(request, 'register.html', {'form': RegisterForm})

def profile_user(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
            return redirect('home')
        
        initial_data = {
            'username': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'phone_number': request.user.phone_number,
            'date_of_birth': request.user.date_of_birth,
            'country': request.user.country,
            'city': request.user.city,
            'street': request.user.street,
            'house_number': request.user.house_number,
            'zip_code': request.user.zip_code                 
        }

        user_orders = Order.objects.filter(user=request.user).order_by('-id')
        paginator = Paginator(user_orders, 10)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)

        context = {
            'form': ProfileForm(initial=initial_data),
            'page': page
            }
        return render(request, 'profile.html', context=context)
    else:
        return redirect('login')
    
def logout_user(request):
    # Clear the cart details upon logout
    response = redirect('home')
    response.delete_cookie('cart')
    logout(request)
    return response