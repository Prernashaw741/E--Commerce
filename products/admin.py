from django.contrib import admin
from .models import Category, Product, ProductVariant

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_active')  # Display key fields
    search_fields = ('name', 'description')  # Allow searching by name or description
    list_filter = ('category', 'is_active')  # Add filtering options
    prepopulated_fields = {'slug': ('name',)}  # Auto-fill slug based on name

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'additional_price', 'stock')  # Show product & variant details