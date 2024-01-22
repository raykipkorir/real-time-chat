from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import SignupForm


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
