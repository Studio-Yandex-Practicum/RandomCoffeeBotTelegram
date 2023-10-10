import enum


class States(str, enum.Enum):
    """Класс, описывающий состояния бота."""

    START = "start"
    ROLE_CHOICE = "role_choice"
    PAIR_SEARCH = "pair_search"
    PAIR_FOUND = "pair_found"
    PAIR_NOT_FOUND = "pair_not_found"
    PROFESSION_CHOICE = "profession_choice"
    PROFILE = "profile"
    NEXT_TIME = "next_time"
    HELP = "help"
    SET_NAME = "set_name"
    SET_NEW_NAME = "set_new_name"
    SET_PHONE_NUMBER = "set_phone_number"
