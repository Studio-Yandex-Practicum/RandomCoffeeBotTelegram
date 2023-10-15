from asgiref.sync import sync_to_async
from django.core.paginator import Paginator
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.buttons import (
    ALL_RIGHT_BUTTON,
    CHANGE_NAME_BUTTON,
    CONTINUE_BUTTON,
    FILL_AGAIN_BUTTON,
    PROFESSION_ANALIST_BUTTON,
    PROFESSION_BACKEND_DEVELOPER_BUTTON,
    PROFESSION_FRONTEND_DEVELOPER_BUTTON,
    PROFESSION_TESTER_BUTTON,
    RECRUITER_ROLE_BUTTON,
    START_BUTTON,
    STUDENT_ROLE_BUTTON,
)
from bot.constants.pagination import PAGE_SEP_SYMBOL, PROFESSION_PER_PAGE
from bot.models import Profession
from bot.utils.pagination import InlineKeyboardPaginator

restart_keyboard_markup = InlineKeyboardMarkup(
    [[InlineKeyboardButton(text=START_BUTTON, callback_data="restart")]]
)

role_choice_keyboard_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text=STUDENT_ROLE_BUTTON, callback_data="student"
            )
        ],
        [
            InlineKeyboardButton(
                text=RECRUITER_ROLE_BUTTON, callback_data="recruiter"
            )
        ],
    ]
)

guess_name_keyboard_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text=CONTINUE_BUTTON, callback_data="continue_name"
            ),
            InlineKeyboardButton(
                text=CHANGE_NAME_BUTTON, callback_data="change_name"
            ),
        ],
    ]
)

profession_choice_keyboard_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text=PROFESSION_ANALIST_BUTTON, callback_data="analyst"
            )
        ],
        [
            InlineKeyboardButton(
                text=PROFESSION_BACKEND_DEVELOPER_BUTTON,
                callback_data="backend-developer",
            )
        ],
        [
            InlineKeyboardButton(
                text=PROFESSION_FRONTEND_DEVELOPER_BUTTON,
                callback_data="frontend-developer",
            )
        ],
        [
            InlineKeyboardButton(
                text=PROFESSION_TESTER_BUTTON, callback_data="tester"
            )
        ],
    ]
)

profile_keyboard_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text=ALL_RIGHT_BUTTON, callback_data="all_right"
            ),
            InlineKeyboardButton(
                text=FILL_AGAIN_BUTTON, callback_data="fill_again"
            ),
        ],
    ]
)


async def build_profession_keyboard(page: int) -> InlineKeyboardPaginator:
    """Создает клавиатуру с пагинацией для выбора профессии."""
    professions = await sync_to_async(list)(
        Profession.objects.all().values("name", "professional_key")
    )
    data_paginator = Paginator(professions, PROFESSION_PER_PAGE)
    telegram_paginator = InlineKeyboardPaginator(
        data_paginator.num_pages,
        current_page=page,
        data_pattern="".join(["continue_name", PAGE_SEP_SYMBOL, "{page}"]),
    )
    for profession in data_paginator.page(page):
        telegram_paginator.add_before(
            InlineKeyboardButton(
                text=profession.get("name"),
                callback_data=profession.get("name"),
            )
        )
    return telegram_paginator
