from django import forms
from django.contrib.auth.hashers import make_password

from admin_user.models import AdminUser
from admin_user.utils.users.registration import generate_random_password


class UserCreationForm(forms.ModelForm):
    """A form for creating new users with random password."""

    class Meta:
        model = AdminUser
        fields = ("email", "username", "first_name", "last_name")

    def save(self, commit=True):
        """Save new user to db with random password."""
        user = super().save(commit=False)
        user.password = make_password(generate_random_password())
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users."""

    class Meta:
        model = AdminUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_superuser",
        )
