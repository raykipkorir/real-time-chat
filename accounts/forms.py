from django.contrib.auth.forms import UserCreationForm
from accounts.models import User


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "profile_pic", "password1", "password2")