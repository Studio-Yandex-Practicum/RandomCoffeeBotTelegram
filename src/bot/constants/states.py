import enum


class States(str, enum.Enum):
    """Класс, описывающий состояния бота."""

    START = "start"
    ROLE_CHOICE = "role_choice"
    PAIR_SEARCH = "pair_search"
    PROFESSION_CHOICE = "profession_choice"
    PROFILE = "profile"
    NEXT_TIME = "next_time"
    HELP = "help"
    FOUND_PAIR = "found_pair"
    SET_NAME = "set_name"
    SET_NEW_NAME = "set_new_name"
    SET_PHONE_NUMBER = "set_phone_number"
    CALLING_IS_SUCCESSFUL = "calling_is_successful"
