from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/chat/user/<str:username>/", consumers.AsyncChatConsumer.as_asgi()),
]
