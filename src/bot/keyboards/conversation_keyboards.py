from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.paginator import Paginator
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.buttons import (ALL_RIGHT_BUTTON, CHANGE_NAME_BUTTON,
                                   CONTINUE_BUTTON, FILL_AGAIN_BUTTON,
                                   IT_SPECIALIST_ROLE_BUTTON, NO_BUTTON,
                                   RECRUITER_ROLE_BUTTON, START_BUTTON,
                                   YES_BUTTON)
from bot.models import Profession
from bot.utils.pagination import InlineKeyboardPaginator

restart_keyboard_markup = InlineKeyboardMarkup(
    [[InlineKeyboardButton(text=START_BUTTON, callback_data="restart")]]
)

role_choice_keyboard_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text=IT_SPECIALIST_ROLE_BUTTON, callback_data="itspecialist"
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
    data_paginator = Paginator(professions, settings.PROFESSION_PER_PAGE)
    telegram_paginator = InlineKeyboardPaginator(
        data_paginator.num_pages,
        current_page=page,
        data_pattern="".join(
            ["continue_name", settings.PAGE_SEP_SYMBOL, "{page}"]
        ),
    )
    for profession in data_paginator.page(page):
        telegram_paginator.add_before(
            InlineKeyboardButton(
                text=profession.get("name"),
                callback_data=profession.get("professional_key"),
            )
        )
    return telegram_paginator


is_pair_successful_keyboard_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text=YES_BUTTON, callback_data="yes"),
            InlineKeyboardButton(text=NO_BUTTON, callback_data="no"),
        ],
    ]
)
