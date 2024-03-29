from django.db import models

from accounts.models import GroupChat, User


class AbstractMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    message_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ["created_at"]


class ChatMessage(AbstractMessage):
    receiver = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="receiver", null=True
    )


class GroupMessage(AbstractMessage):
    receiver = models.ForeignKey(GroupChat, on_delete=models.SET_NULL, null=True)
