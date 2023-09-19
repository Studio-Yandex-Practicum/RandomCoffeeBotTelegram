import enum


class States(str, enum.Enum):
    """Класс, описывающий состояния бота."""

    START = "start"
    ROLE_CHOICE = "role_choice"
    PAIR_SEARCH = "pair_search"
