from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from store.models import Category, Product, Cart, CartItem


class StoreCatalogTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name='Test Electronics',
            slug='test-electronics',
            icon='💻'
        )
        self.product = Product.objects.create(
            category=self.category,
            name='Wireless Earbuds',
            slug='wireless-earbuds',
            description='Crisp audio and noise isolation.',
            price=Decimal('79.99'),
            stock=15
        )

    def test_product_list_status_and_template(self):
        response = self.client.get(reverse('store:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Wireless Earbuds')
        self.assertContains(response, '$79.99')

    def test_category_filter(self):
        response = self.client.get(reverse('store:category_list', args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Wireless Earbuds')

    def test_search_query(self):
        response = self.client.get(reverse('store:product_list') + '?q=Earbuds')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Wireless Earbuds')

        # Negative search
        response2 = self.client.get(reverse('store:product_list') + '?q=NonExistentItemXYZ')
        self.assertEqual(response2.status_code, 200)
        self.assertNotContains(response2, 'Wireless Earbuds')

    def test_product_detail_page(self):
        response = self.client.get(reverse('store:product_detail', args=[self.product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        self.assertContains(response, 'Crisp audio')


class CartTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Gadgets', slug='gadgets')
        self.product = Product.objects.create(
            category=self.category,
            name='Smart Tracker',
            slug='smart-tracker',
            description='Compact GPS tracker.',
            price=Decimal('49.00'),
            stock=10
        )

    def test_add_to_cart_and_update(self):
        # Add to cart
        add_url = reverse('store:cart_add', args=[self.product.id])
        response = self.client.post(add_url, {'quantity': 2}, follow=True)
        self.assertEqual(response.status_code, 200)

        # Check cart item exists
        cart = Cart.objects.first()
        self.assertIsNotNone(cart)
        self.assertEqual(cart.get_total_items(), 2)
        self.assertEqual(cart.get_subtotal(), Decimal('98.00'))

        # Increase quantity via cart_update
        cart_item = cart.items.first()
        update_url = reverse('store:cart_update', args=[cart_item.id])
        self.client.post(update_url, {'action': 'increase'}, follow=True)
        cart.refresh_from_db()
        self.assertEqual(cart.get_total_items(), 3)
        self.assertEqual(cart.get_subtotal(), Decimal('147.00'))

        # Remove item
        remove_url = reverse('store:cart_remove', args=[cart_item.id])
        self.client.post(remove_url, follow=True)
        cart.refresh_from_db()
        self.assertEqual(cart.get_total_items(), 0)

    def test_ajax_add_to_cart(self):
        add_url = reverse('store:cart_add', args=[self.product.id])
        response = self.client.post(
            add_url,
            {'quantity': 1},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['cart_total_items'], 1)
