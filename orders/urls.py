from django.urls import path
from .views import OrderItemListView, OrderListView, OrderDetailView, OrderUpdateStatusView, PaymentView, RazorpayWebhookView
urlpatterns = [
    path('orders/', OrderListView.as_view()),
    path('orders/<int:pk>/', OrderDetailView.as_view()),
    path('orders/<int:order_id>/items/', OrderItemListView.as_view()),
    path('orders/<int:order_id>/update-status/', OrderUpdateStatusView.as_view()),
    path('orders/<int:order_id>/payments/', PaymentView.as_view()),
    path('payments/razorpay/webhook/', RazorpayWebhookView.as_view()),
   
    
]