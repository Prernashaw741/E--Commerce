from rest_framework import serializers
from .models import Product, Category, ProductVariant

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

    
class ProductSerializer(serializers.ModelSerializer):
    Category = CategorySerializer()

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'category', 'description', 'price', 'stock', 'image', 'is_active', 'created_at', 'updated_at']

class ProductVariantSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()

    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'name', 'additional_price', 'stock']

