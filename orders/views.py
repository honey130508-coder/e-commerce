from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from .forms import CheckoutForm
from store.cart_utils import get_or_create_cart


def checkout(request):
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product').all()

    if not cart_items.exists():
        messages.warning(request, "Your cart is currently empty. Add products before checkout!")
        return redirect('store:product_list')

    # Initial form data if user is logged in
    initial_data = {}
    if request.user.is_authenticated:
        initial_data = {
            'full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            'email': request.user.email,
        }

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Check stock for all items
                    for item in cart_items:
                        if item.quantity > item.product.stock:
                            messages.error(
                                request,
                                f"Sorry, only {item.product.stock} units of '{item.product.name}' are available."
                            )
                            return redirect('store:cart_detail')

                    # Create order instance
                    order = form.save(commit=False)
                    if request.user.is_authenticated:
                        order.user = request.user

                    order.subtotal = cart.get_subtotal()
                    order.shipping_cost = cart.get_shipping()
                    order.tax_amount = cart.get_tax()
                    order.total_amount = cart.get_grand_total()
                    order.save()

                    # Create order items and reduce stock
                    for item in cart_items:
                        OrderItem.objects.create(
                            order=order,
                            product=item.product,
                            product_name=item.product.name,
                            product_price=item.product.price,
                            quantity=item.quantity,
                            line_total=item.get_subtotal(),
                        )
                        # Reduce stock
                        item.product.stock -= item.quantity
                        item.product.save()

                    # Clear the cart items
                    cart.items.all().delete()

                messages.success(request, f"Order #{order.order_number} has been placed successfully!")
                return redirect('orders:order_success', order_number=order.order_number)

            except Exception as e:
                messages.error(request, f"An unexpected error occurred during order processing: {str(e)}")
                return redirect('orders:checkout')
    else:
        form = CheckoutForm(initial=initial_data)

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'form': form,
    }
    return render(request, 'orders/checkout.html', context)


def order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'orders/order_success.html', {'order': order})


def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    # Check permissions if order is linked to a user
    if order.user and order.user != request.user and not request.user.is_staff:
        messages.error(request, "You do not have permission to view this order.")
        return redirect('store:product_list')

    return render(request, 'orders/order_detail.html', {'order': order})
