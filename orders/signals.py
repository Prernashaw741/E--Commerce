from django.db.models.signals import post_save, pre_save
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from users.thread_local import get_current_user
from .models import Order, OrderItem


# Send email when an order is created
@receiver(post_save, sender=Order)
def order_created(sender, instance, created, **kwargs):
    if created:
        user = get_current_user()
        if user:
            subject = "Order Confirmation"
            message = f"Thank you {user.first_name}, your order {instance.order_number} has been placed successfully!"
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

# Send email when an order status is updated
@receiver(post_save, sender=Order)
def send_order_status_update_email(sender, instance, **kwargs):
    status_message = {
        "shipped": "Your order has been shipped! Track it using your order number.",
        "out for delivery": "Your order is out for delivery! Expect it soon.",
        "delivered": "Your order has been successfully delivered. Thank you for shopping with us!",
    }

    user = get_current_user()

    if user and instance.status in status_message:
        subject = f"Order {instance.status.capitalize()} Notification"
        message = f"Hi {user.first_name},\n\n{status_message[instance.status]}\n\nOrder Number: {instance.order_number}\n\nBest, \nPrerna"
        recipient_email = user.email

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient_email], fail_silently=False)

# Validate stock before saving order item
@receiver(pre_save, sender=OrderItem)
def check_and_update_product_stock(sender, instance, **kwargs):
    """
    Check if stock is available before saving an order item.
    If available, reduce stock.
    """
    if instance.product.stock < instance.quantity:
        raise ValidationError(f"Not enough stock for {instance.product.name}.")

    # Reduce stock only if validation passes
    instance.product.stock -= instance.quantity
    instance.product.save()
