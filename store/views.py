from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Category, Product, Cart, CartItem
from .cart_utils import get_or_create_cart


@ensure_csrf_cookie
def product_list(request, category_slug=None):
    # Auto-seed sample catalog if database is empty on fresh cloud deploy
    if not Product.objects.exists():
        try:
            from django.core.management import call_command
            call_command('seed_products')
        except Exception:
            pass

    category = None
    products = Product.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    query = request.GET.get('q', '').strip()
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )

    sort_by = request.GET.get('sort', '')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'rating':
        products = products.order_by('-rating')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')

    context = {
        'current_category': category,
        'products': products,
        'query': query,
        'sort_by': sort_by,
        'total_count': products.count(),
    }
    return render(request, 'store/product_list.html', context)


@ensure_csrf_cookie
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)


@ensure_csrf_cookie
def cart_detail(request):
    cart = get_or_create_cart(request)
    context = {
        'cart': cart,
    }
    return render(request, 'store/cart.html', context)


def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1

    if quantity < 1:
        quantity = 1

    if product.stock <= 0:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Sorry, this product is out of stock.'}, status=400)
        messages.error(request, 'Sorry, this product is out of stock.')
        return redirect('store:product_detail', slug=product.slug)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        new_quantity = cart_item.quantity + quantity
        if new_quantity > product.stock:
            cart_item.quantity = product.stock
            cart_item.save()
            msg = f"Adjusted to maximum available stock ({product.stock})."
        else:
            cart_item.quantity = new_quantity
            cart_item.save()
            msg = f"Added {product.name} to your cart."
    else:
        cart_item.quantity = min(quantity, product.stock)
        cart_item.save()
        msg = f"Added {product.name} to your cart."

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': msg,
            'cart_total_items': cart.get_total_items(),
            'cart_subtotal': f"{cart.get_subtotal():.2f}",
        })

    messages.success(request, msg)
    next_url = request.GET.get('next') or request.POST.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('store:cart_detail')


def cart_update(request, item_id):
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

    action = request.POST.get('action')
    try:
        custom_qty = int(request.POST.get('quantity', 0))
    except (ValueError, TypeError):
        custom_qty = 0

    if action == 'increase':
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
            cart_item.save()
        else:
            messages.warning(request, f"Only {cart_item.product.stock} units available.")
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
            cart_item = None
    elif custom_qty > 0:
        cart_item.quantity = min(custom_qty, cart_item.product.stock)
        cart_item.save()
    elif action == 'delete' or custom_qty <= 0:
        cart_item.delete()
        cart_item = None

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'item_removed': cart_item is None,
            'item_quantity': cart_item.quantity if cart_item else 0,
            'item_subtotal': f"{cart_item.get_subtotal():.2f}" if cart_item else "0.00",
            'cart_total_items': cart.get_total_items(),
            'cart_subtotal': f"{cart.get_subtotal():.2f}",
            'shipping': f"{cart.get_shipping():.2f}",
            'tax': f"{cart.get_tax():.2f}",
            'grand_total': f"{cart.get_grand_total():.2f}",
        })

    return redirect('store:cart_detail')


def cart_remove(request, item_id):
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    product_name = cart_item.product.name
    cart_item.delete()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f"Removed {product_name} from your cart.",
            'cart_total_items': cart.get_total_items(),
            'cart_subtotal': f"{cart.get_subtotal():.2f}",
            'shipping': f"{cart.get_shipping():.2f}",
            'tax': f"{cart.get_tax():.2f}",
            'grand_total': f"{cart.get_grand_total():.2f}",
        })

    messages.info(request, f"Removed {product_name} from your cart.")
    return redirect('store:cart_detail')
