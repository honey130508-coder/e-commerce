from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import Category, Product, Cart, CartItem
from orders.models import Order, OrderItem


class OrderProcessingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='shopper',
            email='shopper@example.com',
            password='testpassword123',
            first_name='Alex',
            last_name='Rivera'
        )
        self.category = Category.objects.create(name='Audio', slug='audio')
        self.product = Product.objects.create(
            category=self.category,
            name='Noise Cancelling Headphones',
            slug='noise-cancelling-headphones',
            description='Active noise cancellation.',
            price=Decimal('150.00'),
            stock=5
        )

    def test_checkout_and_order_creation(self):
        # Log in
        self.client.login(username='shopper', password='testpassword123')

        # Add item to cart
        self.client.post(reverse('store:cart_add', args=[self.product.id]), {'quantity': 2})

        # Submit checkout
        checkout_payload = {
            'full_name': 'Alex Rivera',
            'email': 'shopper@example.com',
            'phone': '1234567890',
            'address': '742 Evergreen Terrace',
            'city': 'Springfield',
            'state': 'Oregon',
            'postal_code': '97477',
            'country': 'United States',
            'payment_method': 'Credit Card (Simulation)',
        }
        response = self.client.post(reverse('orders:checkout'), checkout_payload, follow=True)
        self.assertEqual(response.status_code, 200)

        # Check Order in DB
        order = Order.objects.filter(email='shopper@example.com').first()
        self.assertIsNotNone(order)
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.subtotal, Decimal('300.00'))
        self.assertEqual(order.shipping_cost, Decimal('0.00')) # >= 100 is free shipping
        self.assertEqual(order.items.count(), 1)

        # Verify stock was reduced from 5 to 3
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)

        # Check cart is now empty
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 0)

        # Order success page
        success_url = reverse('orders:order_success', args=[order.order_number])
        response2 = self.client.get(success_url)
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, order.order_number)
