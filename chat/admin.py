from django.contrib import admin

from .models import ChatMessage, GroupMessage

admin.site.register(ChatMessage)
admin.site.register(GroupMessage)
