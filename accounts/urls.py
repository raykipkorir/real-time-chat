from django.contrib.auth import views as auth_views
from django.urls import path

from .views import signup_view

urlpatterns = [
    path(
        "",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", signup_view, name="signup"),
]