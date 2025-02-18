from django.urls import path, include
from .views import LoginView

urlpatterns = [
    
    path('google/', LoginView.as_view()),
]
