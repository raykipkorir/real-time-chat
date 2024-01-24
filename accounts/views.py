from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import GroupChatForm, SignupForm
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
        return render(request, "accounts/signup.html", {"form": form})
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
