import enum


class States(str, enum.Enum):
    """111."""

    START = "start"
    ROLE_CHOICE = "role_choice"
    PAIR_SEARCH = "pair_search"
