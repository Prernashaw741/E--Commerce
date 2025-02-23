from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Product, Category, ProductVariant
from .serializers import BulkProductvariantSerializer, ProductSerializer, CategorySerializer, ProductVariantSerializer

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        """
        Custom create method to handle bulk insert of multiple products with variants.
        """
        if isinstance(request.data, list):  # If multiple products
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    lookup_field = 'slug'

class ProductVariantListView(APIView):

    def get(self, request, product_slug, *args, **kwargs):

        try:
            product = Product.objects.get(slug=product_slug)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        variants = ProductVariant.objects.filter(product=product)
        serializer = ProductVariantSerializer(variants, many=True)
        return Response(serializer.data)
    def post(self, request , *args, **kwargs):
        product_slug = kwargs.get('product_slug')

        try:
            product = Product.objects.get(slug=product_slug)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        if isinstance(request.data, list):  # If multiple variants
            for variant in request.data:
                variant['product'] = product.id
            serializer = ProductVariantSerializer(data=request.data, many=True)
        else:
            request.data['product'] = product.id
            serializer = ProductVariantSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

# class ProductVariantListView(generics.ListCreateAPIView):
#     serializer_class = ProductVariantSerializer
        
#     def get_queryset(self):
#         product_slug = self.kwargs['product_slug']
#         return ProductVariant.objects.filter(product__slug=product_slug)

#     def create(self, request, *args, **kwargs):
#         """
#         Custom create method to handle bulk insert of multiple variants.
#         """
#         product_slug = self.kwargs.get('product_slug')
#         try:
#             product = Product.objects.get(slug=product_slug)
#         except Product.DoesNotExist:
#             return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
#         if isinstance(request.data, list):  # If multiple variants
#             for variant in request.data:
#                 variant['product'] = product.id
#             serializer = ProductVariantSerializer(data=request.data, many=True)
#         else:
#             request.data['product'] = product.id
#             serializer = ProductVariantSerializer(data=request.data)

#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)



#     # def get_queryset(self):
#     #     product_slug = self.kwargs['product_slug']
#     #     return ProductVariant.objects.filter(product__slug=product_slug)
    