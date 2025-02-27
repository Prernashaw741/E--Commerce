from django.urls import path, include
from .views import LoginView, OrderHistoryView, AddressDetailView, AddressListView, SetDefaultAddressView


urlpatterns = [
    
    path('google/', LoginView.as_view()),
    path('orders/history/', OrderHistoryView.as_view()),
    path('addresses/', AddressListView.as_view()),
    path('addresses/<int:pk>/', AddressDetailView.as_view()),
    path('addresses/<int:pk>/set-default/', SetDefaultAddressView.as_view()),
]
