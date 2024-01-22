import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from accounts.models import User

from .models import ChatMessage


class AsyncChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.username = self.scope["url_route"]["kwargs"]["username"]
        await database_sync_to_async(self.update_logged_in_user)()
        # self.room_group_name = f"chat_{self.username}"
        # join room group
        # await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # leave room group
        # await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        ...

    # receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        self.message = text_data_json["message"]
        self.receiver_channel_name = await database_sync_to_async(
            self.get_receiver_channel_name
        )()
        self.receiver = await database_sync_to_async(self.get_receiver)()

        await database_sync_to_async(self.create_message)()
        await self.channel_layer.send(
            self.channel_name,
            {
                "type": "chat.message",
                "sender": self.user.username,
                "receiver": self.username,
                "message": self.message,
            },
        )
        if self.receiver_channel_name is not None:
            await self.channel_layer.send(
                self.receiver_channel_name,
                {
                    "type": "chat.message",
                    "sender": self.user.username,
                    "receiver": self.username,
                    "message": self.message,
                },
            )

    def get_receiver_channel_name(self):
        user = User.objects.get(username=self.username)
        return user.channel_name

    def get_receiver(self):
        return User.objects.get(username=self.username)

    def update_logged_in_user(self):
        User.objects.filter(username=self.user.username).update(
            channel_name=self.channel_name
        )
        return None

    def create_message(self):
        return ChatMessage.objects.create(
            sender=self.user, receiver=self.receiver, message_content=self.message
        )

    # receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        receiver = event["receiver"]

        # send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {"message": message, "sender": sender, "receiver": receiver}
            )
        )
