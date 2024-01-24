from django.contrib.auth import views as auth_views
from django.urls import path

from .views import signup_view, group_create_view, join_group

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
    path("create-group/", group_create_view, name="create-group"),
    path("join-group/<str:group_name>/", join_group, name="join-group"),
]
