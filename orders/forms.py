from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    PAYMENT_CHOICES = (
        ('Credit Card (Simulation)', '💳 Credit / Debit Card (Instant Demo)'),
        ('Cash on Delivery', '💵 Cash on Delivery (Pay at Doorstep)'),
        ('PayPal (Simulation)', '🅿️ PayPal (Sandbox)'),
    )

    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'payment-radio'})
    )

    class Meta:
        model = Order
        fields = [
            'full_name', 'email', 'phone', 'address',
            'city', 'state', 'postal_code', 'country', 'payment_method'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Jane Doe'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'jane@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+1 (555) 000-1234'}),
            'address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '123 Market Street, Apt 4B'}),
            'city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'San Francisco'}),
            'state': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'California'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '94103'}),
            'country': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'United States'}),
        }
