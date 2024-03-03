from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import GroupChat, User


class SignupForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    class Meta:
        model = User
        fields = ("username", "profile_pic", "password1", "password2")


class GroupChatForm(forms.ModelForm):
    class Meta:
        model = GroupChat
        fields = ("name", "description", "profile_pic")


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("profile_pic", "username")
