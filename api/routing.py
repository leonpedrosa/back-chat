from django.urls import re_path, path
from . import consumers
from api.fallback_consumer import *


websocket_urlpatterns = [
    re_path(r'ws/teste/$', consumers.HelloConsumer.as_asgi()),
    re_path(r'ws/auth/$', consumers.AuthConsumer.as_asgi()),
    path("", RejectConsumer.as_asgi()),
]
