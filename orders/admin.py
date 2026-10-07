from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'product_price', 'quantity', 'line_total')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'full_name', 'email', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'payment_method')
    search_fields = ('order_number', 'full_name', 'email', 'address')
    list_editable = ('status',)
    inlines = [OrderItemInline]
    readonly_fields = ('order_number', 'created_at', 'updated_at', 'subtotal', 'shipping_cost', 'tax_amount', 'total_amount')
