from django.db.models.signals import post_save
from django.dispatch import receiver

from admin_user.models import AdminUser
from admin_user.utils.reset_password import send_password_reset_email


@receiver(post_save, sender=AdminUser)
def password_reset_email(sender, instance, created, **kwargs):
    """Send email to new admin with link to set password."""
    if not instance.is_staff:
        instance.is_staff = True
        instance.save()
        send_password_reset_email(instance)
