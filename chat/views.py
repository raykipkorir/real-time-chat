from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.models import User

from .models import ChatMessage


@login_required()
def index(request):
    return render(request, "chat/index.html")


@login_required()
def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})


@login_required()
def chat(request):
    users = User.objects.exclude(username=request.user.username)
    return render(request, "chat/chat.html", {"users": users})


@login_required()
def chat_content(request, username):
    users = User.objects.exclude(username=request.user.username)
    messages = ChatMessage.objects.filter(
        sender=request.user, receiver__username=username
    )
    return render(
        request,
        "chat/chat-content.html",
        {"username": username, "messages": messages, "users": users},
    )
