from .models import Category
from .cart_utils import get_or_create_cart

def store_context(request):
    """
    Context processor providing categories and cart item count across all templates.
    """
    categories = Category.objects.all()
    cart_total_items = 0
    try:
        cart = get_or_create_cart(request)
        cart_total_items = cart.get_total_items()
    except Exception:
        cart_total_items = 0

    return {
        'all_categories': categories,
        'cart_total_items': cart_total_items,
    }
