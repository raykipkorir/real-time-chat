from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import GroupChatForm, ProfileUpdateForm, SignupForm
from .models import GroupChat


def signup_view(request):
    if not request.user.is_authenticated:
        form = SignupForm()
        if request.method == "POST":
            form = SignupForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, "Account created successfully")
                return redirect("chat")
        return render(
            request, "accounts/signup.html", {"form": form, "messages": messages}
        )
    else:
        return redirect("chat")


@login_required()
def group_create_view(request):
    groups = GroupChat.objects.exclude(users=request.user)
    form = GroupChatForm()
    if request.method == "POST":
        form = GroupChatForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.created_by = request.user
            group.save()
            group.users.set([request.user])
            return redirect("group-chat", group_name=group.name)
    return render(request, "accounts/join-group.html", {"form": form, "groups": groups})


@login_required()
def join_group(request, group_name):
    group = GroupChat.objects.get(name=group_name)
    group.users.add(request.user)
    return redirect("group-chat", group_name=group_name)


class CustomPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    success_message = "Password changed successfully"
    success_url = reverse_lazy("chat")


@login_required()
def user_update(request):
    form = ProfileUpdateForm(instance=request.user)
    if request.method == "POST":
        form = ProfileUpdateForm(
            data=request.POST, files=request.FILES, instance=request.user
        )
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully")
            return redirect("user_update")
    return render(request, "accounts/user_update.html", {"form": form})


@login_required()
def user_delete(request):
    if request.method == "POST":
        request.user.delete()
        return redirect("login")
    return render(request, "accounts/user_delete.html")
