from channels.generic.websocket import WebsocketConsumer
import logging

logger = logging.getLogger(__name__)

class RejectConsumer(WebsocketConsumer):
    def connect(self):
        logger.warning(f"WebSocket rejeitado para rota inválida: {self.scope['path']}")
        self.close()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        pass
