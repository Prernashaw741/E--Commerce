from rest_framework import serializers
from .models import Order, Address, OrderHistory

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["id", "user", "street_address", "city", "state", "postal_code", "country", "is_default"]
        read_only_fields = ["user"]

class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderHistory
        fields = ["id", "user", "order", "created_at"]
        read_only_fields = ["user", "order"]

