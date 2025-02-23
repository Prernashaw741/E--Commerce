from django.contrib import admin
from .models import Order, OrderItem, Payment

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_number', 'status', 'total_price', 'created_at')
    search_fields = ('user__email', 'order_number', 'status')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'variant', 'quantity', 'price')
    search_fields = ('product__name', 'order__user__email')
    list_filter = ('order__status',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_method', 'transaction_id', 'is_successful', 'created_at')
    search_fields = ('order__order_number', 'transaction_id')
    list_filter = ('payment_method', 'is_successful', 'created_at')
