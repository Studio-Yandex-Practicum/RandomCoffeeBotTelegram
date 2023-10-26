from django.urls import path

from admin_user.views import PasswordSetView

app_name = "admin_user"

urlpatterns = [
    path(
        "set_password/<uidb64>/<token>/",
        PasswordSetView.as_view(),
        name="password_set",
    ),
]
