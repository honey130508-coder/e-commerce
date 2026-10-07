from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm
from store.cart_utils import get_or_create_cart
from orders.models import Order


def register_view(request):
    if request.user.is_authenticated:
        return redirect('store:product_list')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Merge any session cart
            get_or_create_cart(request)
            messages.success(request, f"Welcome to our store, {user.first_name or user.username}! Your account has been created.")
            next_url = request.GET.get('next') or 'store:product_list'
            return redirect(next_url)
    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('store:product_list')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Merge session cart
            get_or_create_cart(request)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.POST.get('next') or request.GET.get('next') or 'store:product_list'
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = UserLoginForm()

    next_url = request.GET.get('next', '')
    return render(request, 'accounts/login.html', {'form': form, 'next': next_url})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "You have been logged out.")
    return redirect('store:product_list')


@login_required
def orders_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/orders_history.html', {'orders': orders})
