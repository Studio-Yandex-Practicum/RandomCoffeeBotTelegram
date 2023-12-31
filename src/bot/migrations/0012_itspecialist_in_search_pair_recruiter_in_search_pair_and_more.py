# Generated by Django 4.2.6 on 2023-11-25 11:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bot", "0011_add_messages_in_messagebot"),
    ]

    operations = [
        migrations.AddField(
            model_name="itspecialist",
            name="in_search_pair",
            field=models.BooleanField(default=False, verbose_name="В поиске пары"),
        ),
        migrations.AddField(
            model_name="recruiter",
            name="in_search_pair",
            field=models.BooleanField(default=False, verbose_name="В поиске пары"),
        ),
        migrations.AlterField(
            model_name="messagebot",
            name="message",
            field=models.TextField(
                help_text="Не удаляйте '{}'. Это метка для вставки динамических данных.",
                unique=True,
                verbose_name="Текст сообщения бота",
            ),
        ),
    ]
