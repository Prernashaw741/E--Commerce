from rest_framework import serializers
from .models import Product, Category, ProductVariant

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

    
# class ProductVariantSerializer(serializers.ModelSerializer):
#     product = serializers.StringRelatedField()

#     class Meta:
#         model = ProductVariant
#         fields = ['id', 'product', 'name', 'additional_price', 'stock']

# class ProductSerializer(serializers.ModelSerializer):
#     category = serializers.SlugRelatedField(
#         queryset=Category.objects.all(),
#         slug_field='slug'
#     )
#     variants = ProductVariantSerializer(many=True, required=False)

#     class Meta:
#         model = Product
#         fields = '__all__'

#     # def create(self, validated_data):
#     #     if isinstance(validated_data, list):
#     #         return Product.objects.bulk_create([Product(**item) for item in validated_data])
#     #     return super().create(validated_data)

#     def create(self, validated_data):
#         variants_data = validated_data.pop('variants', [])
#         product = Product.objects.create(**validated_data)
#         for variant_data in variants_data:
#             ProductVariant.objects.create(product=product, **variant_data)
#         return product



class ProductVariantSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=False)
    class Meta:
        model = ProductVariant
        fields = ['id', 'name', 'additional_price', 'stock', 'product']

class BulkProductvariantSerializer(serializers.Serializer):
    variants = ProductVariantSerializer(many=True)

    def create(self, validated_data):
        variants_data = validated_data.pop('variants')
        product = validated_data.get('product')
        product_variants = []
        for variant in variants_data:
            product_variants.append(ProductVariant(product=product, **variant))
        return ProductVariant.objects.bulk_create(product_variants)

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    variants = ProductVariantSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'category', 'description', 'price', 'stock', 'is_active', 'variants']

    def create(self, validated_data):
        variants_data = validated_data.pop('variants', [])  # Extract variants

        # 🔹 **Check if product already exists**
        product, created = Product.objects.get_or_create(
            slug=validated_data["slug"],
            category=validated_data["category"],
            defaults=validated_data  # If not exists, create it
        )

        # 🔹 **Only add variants if the product was newly created**
        if created:
            for variant in variants_data:
                ProductVariant.objects.create(product=product, **variant)

        return product
