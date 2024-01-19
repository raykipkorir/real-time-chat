from django.urls import path

from . import views

urlpatterns = [
    path("join-group/", views.index, name="join-group"),
    path("", views.chat, name="chat"),
    path("user/<str:username>/", views.chat_content, name="chat-content"),
    path("group/<str:room_name>/", views.room, name="room"),
]
