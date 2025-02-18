from django.urls import path
from .views import CategoryListView, CategoryDetailView, ProductListView, ProductDetailView, ProductVariantListView

urlpatterns = [
    path('categories/', CategoryListView.as_view()),
    path('categories/<slug:slug>/', CategoryDetailView.as_view()),
    path('products/', ProductListView.as_view()),
    path('products/<slug:slug>/', ProductDetailView.as_view()),
    path('products/<slug:product_slug>/variants/', ProductVariantListView.as_view()),
]
