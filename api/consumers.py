from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import uuid


class HelloConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        self.send(text_data='Hello, I am alive')


class AuthConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        from django.contrib.auth.models import AnonymousUser
        user = self.scope.get("user", AnonymousUser())
        if user.is_authenticated:
            await self.accept()
            self.connect_id = str(uuid.uuid4())
            await self.send(text_data=json.dumps({
                "type": "connected",
                "connection_id": self.connect_id,
                "user": {
                    "id": user.id,
                    "avatar": "https://cdn.quasar.dev/img/avatar1.jpg",
                    "is_online": True,
                    "username": user.username
                }
            }))
        else:
            # TODO: Realizar login tbm via websocket
            await self.close()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        await self.send(text_data=json.dumps({
            "echo": text_data
        }))