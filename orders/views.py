from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.crypto import get_random_string

from orders.permissions import IsOwner

from users.models import OrderHistory, User
from .models import Order, OrderItem, Payment
from .serializers import OrderSerializer, OrderItemSerializer, PaymentSerializer
from users.utils import send_email

from django.conf import settings
from django.core.mail import send_mail


class OrderListView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.COOKIES.get("uid"))
    
    def create(self, request, *args, **kwargs):
        order_data = request.data
        order_items = order_data.pop("items", [])

        # Fetch user from cookies
        user_id = request.COOKIES.get("uid")
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Generate a unique order number
        order_number = get_random_string(10).upper()

        # Create the order
        order = Order.objects.create(
            user=User.objects.get(id=request.COOKIES.get("uid")), 
            order_number=order_number, 
            status = "PENDING",
            total_price=0.0
        )

        total_price = 0.0
        created_items = []

        # create order items
        for item in order_items:
            item["order"] = order.id
            serializer = OrderItemSerializer(data=item)
            if serializer.is_valid():
                order_item = serializer.save()
                total_price += order_item.price * order_item.quantity
                created_items.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        # Update the order total price
        order.total_price = total_price 
        order.save()

        # Send email to user
        send_email(
            subject="Order Confirmation",
            message=f"Hi {user.first_name},\n\nYour order has been placed successfully! Order number: {order_number}\n\nTotal: {total_price}\n\nBest, \nPrerna",
            from_email = settings.DEFAULT_FROM_EMAIL,
            recipient_email = order.user.email,
            fail_silently=False
        )

       

        return Response({
            "order": OrderSerializer(order).data,
            "items": created_items
        }, status=status.HTTP_201_CREATED)
    
class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsOwner]

class OrderUpdateStatusView(APIView):
    permission_classes = [IsOwner]

    
    def patch(self, request, order_id):

        try:
            order = Order.objects.get(id = order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        
        
        
        new_status = request.data.get("status")

        status_message = {
            "shipped": "Your order has been shipped! Track it using your order number.",
            "out for delivery": "Your order is out for delivery! Expect it soon.",
            "delivered": "Your order has been successfully delivered. Thank you for shopping with us!",
        }

        
        # Fetch user from cookies
        user_id = request.COOKIES.get("uid")
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if new_status in status_message:
            print("Sending status update email to:", user.email)

            send_email(
                subject=f"Order {new_status.capitalize()} Notification", 
                message=f"Hi {user.first_name},\n\n{status_message[new_status]}\n\nOrder Number: {order.order_number}\n\nBest, \nPrerna",
                from_email = settings.DEFAULT_FROM_EMAIL,
                recipient_email = user.email,
                fail_silently=False
            )

        

        if new_status not in dict(Order.STATUS_CHOICES):
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = new_status
        order.save()

        if new_status in ["delivered", "cancelled"]:
            OrderHistory.objects.create(user=order.user, order=order)

        return Response({"message": f"Order status updated {new_status}"}, status=status.HTTP_200_OK)
    
    
class OrderItemListView(generics.ListAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        order_id = self.kwargs.get("order_id")
        return OrderItem.objects.filter(order_id=order_id)
    
class PaymentView(APIView):
    permission_classes = [IsOwner]
    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user = request.COOKIES.get("uid"))
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if Payment.objects.filter(order=order).exists():
            return Response({"error": "Payment already exists for this order"}, status=status.HTTP_400_BAD_REQUEST)
        payment_data = request.data
        payment_data["order"] = order.id

        serializer = PaymentSerializer(data=payment_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Payment successful", "payment": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, order_id):
        try:
            payment = Payment.objects.get(order_id=order_id, order__user=request.COOKIES.get("uid"))
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(PaymentSerializer(payment).data, status=status.HTTP_200_OK)
        
