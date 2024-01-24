from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    channel_name = models.CharField(max_length=500, blank=True, null=True)
    profile_pic = models.ImageField(upload_to="profile_pics", blank=True, null=True)


class GroupChat(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to="profile_pics", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    users = models.ManyToManyField(User, related_name="group_users")

    def __str__(self):
        return self.name
