# Generated by Django 4.2.6 on 2023-11-25 22:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bot", "0011_add_messages_in_messagebot"),
    ]

    operations = [
        migrations.AlterField(
            model_name="itspecialist",
            name="last_login_date",
            field=models.DateTimeField(
                auto_now=True, verbose_name="Заходил в последний раз"
            ),
        ),
        migrations.AlterField(
            model_name="itspecialist",
            name="registration_date",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="Дата регистрации"
            ),
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
        migrations.AlterField(
            model_name="recruiter",
            name="last_login_date",
            field=models.DateTimeField(
                auto_now=True, verbose_name="Заходил в последний раз"
            ),
        ),
        migrations.AlterField(
            model_name="recruiter",
            name="registration_date",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="Дата регистрации"
            ),
        ),
    ]
