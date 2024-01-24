from django.urls import path

from . import views

urlpatterns = [
    path("", views.chat, name="chat"),
    path("user/<str:username>/", views.private_chat, name="private-chat"),
    path("group/<str:group_name>/", views.group_chat, name="group-chat"),
]
