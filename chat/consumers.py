import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from accounts.models import GroupChat, User

from .models import ChatMessage, GroupMessage


class AsyncChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.username = self.scope["url_route"]["kwargs"]["username"]
        await self.update_logged_in_user()

        await self.accept()

    async def disconnect(self, close_code):
        ...

    # receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        self.message = text_data_json["message"]
        self.receiver_channel_name = await self.get_receiver_channel_name()

        await self.create_message()
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

    @database_sync_to_async
    def get_receiver_channel_name(self):
        user = User.objects.get(username=self.username)
        return user.channel_name

    @database_sync_to_async
    def update_logged_in_user(self):
        User.objects.filter(username=self.user.username).update(
            channel_name=self.channel_name
        )
        return None

    @database_sync_to_async
    def create_message(self):
        receiver = User.objects.get(username=self.username)
        return ChatMessage.objects.create(
            sender=self.user, receiver=receiver, message_content=self.message
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


class AsyncGroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.group_name = self.scope["url_route"]["kwargs"]["group_name"]
        # join room group
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # leave room group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        self.message = text_data_json["message"]

        await self.create_message()
        # Send message to room group
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat.message",
                "message": self.message,
                "sender": self.user.username,
                "group_name": self.group_name,
            },
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        group_name = event["group_name"]

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {"message": message, "sender": sender, "group_name": group_name}
            )
        )

    @database_sync_to_async
    def create_message(self):
        group = GroupChat.objects.get(name=self.group_name)
        return GroupMessage.objects.create(
            sender=self.user, receiver=group, message_content=self.message
        )
