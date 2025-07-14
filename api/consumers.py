from json import JSONDecodeError
from asgiref.sync import sync_to_async
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from api.presence import mark_online, mark_offline
import json
import uuid


class HelloConsumer(WebsocketConsumer):
    """Um consumer simples de teste, apenas responde 'I am alive'."""
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        self.send(text_data='Hello, I am alive')


class AuthConsumer(AsyncWebsocketConsumer):
    """
    Consumer principal da aplicação, gerencia:
    - Autenticação do websocket (via JWT)
    - Marcação de presença (online/offline)
    - Envio de mensagens de presença para outros clientes via group_send
    """

    async def connect(self):
        # Recupera o usuário da conexão WebSocket
        from django.contrib.auth.models import AnonymousUser
        user = self.scope.get("user", AnonymousUser())
        if user.is_authenticated:
            await self.accept()
            self.user_id = user.id
            self.connect_id = str(uuid.uuid4())

            # Marca como online
            await sync_to_async(mark_online)(user.id)

            # Adicionar no grupo de presenca
            await self.channel_layer.group_add("presence", self.channel_name)

            # Envia notificação para os outros
            await self.notify_presence(user.id, True)

            await self.send(text_data=json.dumps({
                "type": "connected",
                "connection_id": self.connect_id,
                "user": {
                    "id": user.id,
                    "is_online": True,
                    "username": user.username
                }
            }))
        else:
            # TODO: Realizar login tbm via websocket
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, 'user_id'):
            await sync_to_async(mark_offline)(self.user_id)
            # Remove do grupo
            await self.channel_layer.group_discard("presence", self.channel_name)
            # Notificação para outros que o usuário saiu
            await self.notify_presence(self.user_id, False)

    async def receive(self, text_data):
        """
        Recebe mensagens do webSocket, trata keepalive e ecoa outras mensagens
        """
        try:
            data = json.loads(text_data)
        except JSONDecodeError:
            data = {}
        if data.get("type") == "keepalive" and hasattr(self, "user_id"):
            await sync_to_async(mark_online)(self.user_id)
        else:
            await self.send(text_data=json.dumps({
                "echo": data
            }))

    async def notify_presence(self, user_id, is_online):
        channels_layer = get_channel_layer()
        await channels_layer.group_send(
            "presence", {
                "type": "user.presence",
                "user_id": user_id,
                "is_online": is_online
            }
        )

    async def user_presence(self, event):
        await self.send(text_data=json.dumps({
            "type": "presence",
            "user_id": event["user_id"],
            "is_online": event["is_online"]
        }))
