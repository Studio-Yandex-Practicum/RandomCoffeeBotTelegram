from bot.models import FormUrl


async def get_form_url(key):
    """Получение ссылки на форму по ключу."""
    form_url = await FormUrl.objects.aget(url_key=key)
    return form_url.url
