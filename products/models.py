from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Category Name")
    slug = models.SlugField(unique=True, verbose_name="Category Slug")

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Product Name")
    slug = models.SlugField(verbose_name="Product Slug")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", verbose_name="Product Category")
    description = models.TextField(verbose_name="Product Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Product Price")
    stock = models.PositiveIntegerField(verbose_name="Stock Quantity")
    image = models.ImageField(upload_to="product_images/", blank=True, null=True, verbose_name="Product Image")
    is_active = models.BooleanField(default=True, verbose_name="Product Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        unique_together = ['slug', 'category']

    def __str__(self):
        return f"{self.name} ({self.category.name})"
    



class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants", verbose_name="Parent Product")
    name = models.CharField(max_length=255, verbose_name="Variant Name")  
    additional_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Additional Price")  
    stock = models.PositiveIntegerField(verbose_name="Stock Quantity")

    def __str__(self):
        return f"{self.product.name} - {self.name}"
