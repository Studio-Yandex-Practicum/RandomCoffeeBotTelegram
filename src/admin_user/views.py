from django.contrib import messages
from django.contrib.auth.models import Permission
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy


class PasswordSetView(PasswordResetConfirmView):
    """User password reset view."""

    success_url = reverse_lazy("admin:index")

    def form_valid(self, form):
        """Set user satus as active if password was changed."""
        response = super().form_valid(form)
        messages.success(self.request, "Пароль был успешно изменен.")
        self.user.is_staff = True
        permissions = Permission.objects.all()
        for permission in permissions:
            self.user.user_permissions.add(permission)
        self.user.save()
        return response
