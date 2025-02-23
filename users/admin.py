from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import Address, Wishlist, OrderHistory

User = get_user_model()  # Get the custom User model

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'phone_number', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('email', 'username', 'phone_number')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    ordering = ('-date_joined',)
    fieldsets = (
        ("Personal Info", {"fields": ("email", "username", "phone_number", "profile_picture")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        ("Create User", {
            "classes": ("wide",),
            "fields": ("email", "username", "phone_number", "password1", "password2"),
        }),
    )

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'street_address', 'city', 'state', 'postal_code', 'country', 'is_default')
    search_fields = ('user__email', 'city', 'state', 'postal_code')
    list_filter = ('country', 'is_default')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
    search_fields = ('user__email', 'product__name')

@admin.register(OrderHistory)
class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'order')
    search_fields = ('user__email', 'order__order_number')
 