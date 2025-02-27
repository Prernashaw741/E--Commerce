from rest_framework import serializers
from .models import Order, OrderItem, Payment

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "variant", "quantity", "price"]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "user", "order_number", "status", "total_price", "created_at", "updated_at", "items"]

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "order", "payment_method", "transaction_id", "is_successful", "created_at"]
        
# class AddressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Address
#         fields = ["id", "user", "street_address", "city", "state", "postal_code", "country", "is_default"]
#         read_only_fields = ["user"]

# class OrderHistorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderHistory
#         fields = ["id", "user", "order", "created_at"]
#         read_only_fields = ["user", "order"]