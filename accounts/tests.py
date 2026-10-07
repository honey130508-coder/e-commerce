from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class AccountsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_registration(self):
        register_url = reverse('accounts:register')
        payload = {
            'username': 'newbuyer',
            'first_name': 'Buyer',
            'last_name': 'One',
            'email': 'buyer@example.com',
            'password': 'safePassword123',
            'confirm_password': 'safePassword123',
        }
        response = self.client.post(register_url, payload, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newbuyer').exists())
        user = User.objects.get(username='newbuyer')
        self.assertEqual(user.email, 'buyer@example.com')

    def test_user_login_and_logout(self):
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='secretPassword123'
        )

        login_url = reverse('accounts:login')
        response = self.client.post(login_url, {
            'username': 'existinguser',
            'password': 'secretPassword123',
        }, follow=True)
        self.assertEqual(response.status_code, 200)

        # Check logged in state via orders history access
        history_url = reverse('accounts:orders_history')
        response2 = self.client.get(history_url)
        self.assertEqual(response2.status_code, 200)

        # Logout
        logout_url = reverse('accounts:logout')
        response3 = self.client.post(logout_url, follow=True)
        self.assertEqual(response3.status_code, 200)
