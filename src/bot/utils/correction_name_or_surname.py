import re

from bot.constants.models import MAX_LEN_NAME_AND_SURNAME
from bot.constants.patterns import HTML_TEG_PATTERN


def correction_name_or_surname(name: str) -> str:
    """Удаление тегов HTML в имени/фамилии."""
    pattern = re.compile(HTML_TEG_PATTERN)
    name = re.sub(pattern, "", name)[:MAX_LEN_NAME_AND_SURNAME]
    if not name:
        name = "unknown"
    return name
