from asgiref.sync import sync_to_async

from bot.models import FormUrl


async def get_form_url(key):
    """Получение ссылки на форму по ключу."""
    form_url = await sync_to_async(FormUrl.objects.get)(url_key=key)
    return form_url.url
