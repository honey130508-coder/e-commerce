from .models import Cart, CartItem

def get_or_create_cart(request):
    """
    Retrieves the cart for the current user or session.
    If the user has logged in, any anonymous session cart is merged into the user's cart.
    """
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    if request.user.is_authenticated:
        # Check if there is a session-based cart to merge
        user_cart, _ = Cart.objects.get_or_create(user=request.user)
        session_cart = Cart.objects.filter(session_key=session_key, user__isnull=True).first()
        
        if session_cart and session_cart != user_cart:
            for item in session_cart.items.all():
                user_item, created = CartItem.objects.get_or_create(
                    cart=user_cart,
                    product=item.product,
                    defaults={'quantity': item.quantity}
                )
                if not created:
                    user_item.quantity += item.quantity
                    user_item.save()
            session_cart.delete()
        return user_cart
    else:
        cart, _ = Cart.objects.get_or_create(session_key=session_key)
        return cart
