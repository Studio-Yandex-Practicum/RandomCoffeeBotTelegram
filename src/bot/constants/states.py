import enum


class States(str, enum.Enum):
    """Класс, описывающий состояния бота."""

    START = "start"
    ROLE_CHOICE = "role_choice"
    PAIR_SEARCH = "pair_search"
    NEXT_TIME = "next_time"
    HELP = "help"
    SET_NAME = "set_name"
    SET_NEW_NAME = "set_new_name"
