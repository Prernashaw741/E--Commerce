from rest_framework import generics
from .models import Product, Category, ProductVariant
from .serializers import ProductSerializer, CategorySerializer, ProductVariantSerializer

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    lookup_field = 'slug'

class ProductVariantListView(generics.ListAPIView):
    serializer_class = ProductVariantSerializer
    def get_queryset(self):
        product_slug = self.kwargs['product_slug']
        return ProductVariant.objects.filter(product__slug=product_slug)
    