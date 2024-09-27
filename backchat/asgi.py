import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from api import consumers
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backchat.settings')

# application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/chat/", consumers.ChatConsumer.as_asgi()),
        ])
    ),
})