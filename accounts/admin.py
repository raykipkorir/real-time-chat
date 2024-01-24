from django.contrib import admin

from .models import GroupChat, User

admin.site.register(User)
admin.site.register(GroupChat)
