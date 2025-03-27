"""
ASGI config for ecom project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import ecom.routing  # Required for websocket_urlpatterns in ProtocolTypeRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')

# django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket":AuthMiddlewareStack(
        URLRouter(
            ecom.routing.websocket_urlpatterns
        )
    ),
})
