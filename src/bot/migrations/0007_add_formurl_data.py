# Generated by Django 4.2.6 on 2023-10-11 13:46

from django.db import migrations


def create_url_support(apps, schema_editor):
    """Create FormUrl 'Support'."""
    FormUrl = apps.get_model("bot", "FormUrl")
    FormUrl.objects.create(
        title="Поддержка",
        url_key="support"
    )


def remove_url_support(apps, schema_editor):
    """Remove FormUrl 'Support' instance."""
    FormUrl = apps.get_model("bot", "FormUrl")
    remove_form_url = FormUrl.objects.get(url_key="support")
    remove_form_url.delete()


def create_url_guide(apps, schema_editor):
    """Create FormUrl 'Guide'."""
    FormUrl = apps.get_model("bot", "FormUrl")
    FormUrl.objects.create(
        title="Гайд",
        url_key="guide"
    )


def remove_url_guide(apps, schema_editor):
    """Remove FormUrl 'Guide' instance."""
    FormUrl = apps.get_model("bot", "FormUrl")
    remove_form_url = FormUrl.objects.get(url_key="guide")
    remove_form_url.delete()


def create_url_feedback(apps, schema_editor):
    """Create FormUrl 'Feedback'."""
    FormUrl = apps.get_model("bot", "FormUrl")
    FormUrl.objects.create(
        title="Обратная связь",
        url_key="feedback"
    )


def remove_url_feedback(apps, schema_editor):
    """Remove FormUrl 'Feedback' instance."""
    FormUrl = apps.get_model("bot", "FormUrl")
    remove_form_url = FormUrl.objects.get(url_key="feedback")
    remove_form_url.delete()


class Migration(migrations.Migration):
    dependencies = [
        ('bot', '0006_add_formurl_model'),
    ]

    operations = [
        migrations.RunPython(
            create_url_support,
            reverse_code=remove_url_support
        ),
        migrations.RunPython(
            create_url_guide,
            reverse_code=remove_url_guide
        ),
        migrations.RunPython(
            create_url_feedback,
            reverse_code=remove_url_feedback
        ),
    ]
