# Generated by Django 4.2.5 on 2023-09-22 08:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bot", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="recruiter",
            name="waiting_time",
            field=models.DateField(
                auto_now_add=True, null=True, verbose_name="Время ожидания пары"
            ),
        ),
        migrations.AddField(
            model_name="student",
            name="waiting_time",
            field=models.DateField(
                auto_now_add=True, null=True, verbose_name="Время ожидания пары"
            ),
        ),
    ]
