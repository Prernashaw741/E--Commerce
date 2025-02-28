from rest_framework import serializers
from .models import Address, OrderHistory, Wishlist
from products.models import Product

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

class WishlistSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Wishlist
        fields = ["id", "user", "product", "product_name"]
        read_only_fields = ["user"]