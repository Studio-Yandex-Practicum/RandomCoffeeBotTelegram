from django.core.validators import RegexValidator

from bot.constants.patterns import MESSAGE_KEY_PATTERN


def validator_message_key() -> RegexValidator:
    """Валидатор ключа сообщения бота."""
    return RegexValidator(
        MESSAGE_KEY_PATTERN,
        message=(
            "Ключ должен стостоять только из латинских "
            "букв, цифр и знака подчеркивания"
        ),
        code="Invalid key",
    )
