from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from accounts.models import User, GroupChat

from .models import ChatMessage, GroupMessage


@login_required()
def chat(request):
    users = User.objects.exclude(username=request.user.username)
    groups = GroupChat.objects.filter(users=request.user)
    return render(request, "chat/chat.html", {"users": users, "groups": groups})


@login_required()
def private_chat(request, username):
    receiver = User.objects.get(username=username)
    users = User.objects.exclude(username=request.user.username)
    groups = GroupChat.objects.filter(users=request.user)
    chat_messages = ChatMessage.objects.select_related("sender", "receiver").filter(
        Q(sender=request.user, receiver__username=username)
        | Q(sender__username=username, receiver__username=request.user)
    )
    return render(
        request,
        "chat/private-chat.html",
        {
            "chat_messages": chat_messages,
            "users": users,
            "groups": groups,
            "receiver": receiver,
        },
    )


@login_required()
def group_chat(request, group_name):
    group = GroupChat.objects.prefetch_related("users").get(name=group_name)
    members = group.users.all()
    users = User.objects.exclude(username=request.user.username)
    groups = GroupChat.objects.prefetch_related("created_by", "users").filter(
        users=request.user
    )
    chat_messages = GroupMessage.objects.select_related("sender", "receiver").filter(
        receiver=group
    )
    return render(
        request,
        "chat/group-chat.html",
        {
            "group": group,
            "users": users,
            "groups": groups,
            "members": members,
            "chat_messages": chat_messages,
        },
    )
