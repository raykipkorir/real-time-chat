from django.contrib.auth import views as auth_views
from django.urls import path, include

from .views import (
    signup_view,
    group_create_view,
    join_group,
    CustomPasswordChangeView,
    user_update,
    user_delete,
)

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("create-group/", group_create_view, name="create-group"),
    path("join-group/<str:group_name>/", join_group, name="join-group"),
    # login and logout
    path(
        "",
        auth_views.LoginView.as_view(
            template_name="registration/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # settings
    path(
        "settings/",
        include(
            [
                path("", user_update, name="user_update"),
                path("user/", user_update, name="user_update"),
                path("delete-user/", user_delete, name="user_delete"),
                path(
                    "password_change/",
                    CustomPasswordChangeView.as_view(),
                    name="password_change",
                ),
                path(
                    "password_reset/",
                    auth_views.PasswordResetView.as_view(),
                    name="password_reset",
                ),
                path(
                    "password_reset_done/",
                    auth_views.PasswordResetDoneView.as_view(),
                    name="password_reset_done",
                ),
                path(
                    "reset/<uidb64>/<token>/",
                    auth_views.PasswordResetConfirmView.as_view(),
                    name="password_reset_confirm",
                ),
                path(
                    "reset/done/",
                    auth_views.PasswordResetCompleteView.as_view(),
                    name="password_reset_complete",
                ),
            ]
        ),
    ),
]
