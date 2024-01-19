import json

from channels.auth import login
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from accounts.models import User

from .models import ChatMessage


class AsyncChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.username = self.scope["url_route"]["kwargs"]["username"]
        self.room_group_name = f"chat_{self.username}"

        # join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    # async def disconnect(self, close_code):
    #     # leave room group
    #     await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # receive message from WebSocket
    async def receive(self, text_data):
        # await login(self.scope, self.user)

        text_data_json = json.loads(text_data)
        self.message = text_data_json["message"]
        self.receiver = await database_sync_to_async(self.get_receiver)()
        await database_sync_to_async(self.create_message)()
        # send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": self.message}
        )
        # await database_sync_to_async(self.scope["session"].save)()

    def get_receiver(self):
        return User.objects.get(username=self.username)

    def create_message(self):
        return ChatMessage.objects.create(
            sender=self.user, receiver=self.receiver, message_content=self.message
        )

    # receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
