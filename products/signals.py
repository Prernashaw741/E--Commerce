from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product
from django.core.cache import cache
from django.core.cache import caches

@receiver([post_save, post_delete], sender=Product)
def invalidate_product_cache(sender, instance, **kwargs):
    print("Clearing product cache")
    
    # clear product list cache
    cache.delete_pattern('*product_list*')
    # cache.delete('product_list')
    # cache.clear(prefix='product_list')
    # caches.
    # cache.delete_many(keys=['product_list'])