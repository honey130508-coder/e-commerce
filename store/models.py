import uuid
from decimal import Decimal
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, default="🏷️", help_text="Emoji or icon")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=10)
    image_url = models.URLField(max_length=500, blank=True, default='')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5)
    rating_count = models.PositiveIntegerField(default=18)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

    def get_image(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return "/static/images/placeholder.svg"

    @property
    def is_in_stock(self):
        return self.stock > 0


class Cart(models.Model):
    session_key = models.CharField(max_length=40, blank=True, null=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"Cart ({self.user.username})"
        return f"Cart (Session: {self.session_key})"

    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())

    def get_subtotal(self):
        return sum(item.get_subtotal() for item in self.items.all())

    def get_shipping(self):
        subtotal = self.get_subtotal()
        if subtotal == 0 or subtotal >= Decimal('100.00'):
            return Decimal('0.00')
        return Decimal('10.00')

    def get_tax(self):
        return (self.get_subtotal() * Decimal('0.08')).quantize(Decimal('0.01'))

    def get_grand_total(self):
        return self.get_subtotal() + self.get_shipping() + self.get_tax()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_subtotal(self):
        return self.product.price * self.quantity
