# Generated by Django 4.2.6 on 2023-11-24 00:50

from django.db import migrations


def create_messages(apps, schema_editor):
    """Создание сообщений бота."""
    MessageBot = apps.get_model("bot", "MessageBot")
    messages = (
        MessageBot(title="Отсутвие в зарегистрированных",
                   message=(
                        "Вас нет в зарегистрированных\n"
                        "пользователях, для того, чтобы начать\n"
                        "нажмите /start"
                    ),
                   message_key="not_registred_message"),
        MessageBot(title="Подтверждение удаления аккаунта",
                   message=(
                        "Ваша профессия {}.\n" "Хотите удалить аккаунт?"
                    ),
                   message_key="confirmation_delete_account_message"),
        MessageBot(title="Сообщение об удалении",
                   message=(
                    "Ваш аккаунт удален, если хотите\n"
                    "продолжить нажмите /start"
                   ),
                   message_key="account_deleted_message"),
    )
    MessageBot.objects.bulk_create(messages)


def remove_messages(apps, schema_editor):
    """Удаление сообщений бота."""
    MessageBot = apps.get_model("bot", "MessageBot")
    MessageBot.objects.filter(
        message_key__in=("not_registred_message",
                         "confirmation_delete_account_message",
                         "account_deleted_message")
        ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("bot", "0012_alter_itspecialist_last_login_date_and_more"),
    ]

    operations = [
        migrations.RunPython(
            create_messages,
            reverse_code=remove_messages
        )
    ]
