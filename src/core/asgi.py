import os

from django_asgi_lifespan.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.config.settings_base")

django_application = get_asgi_application()


async def application(scope, receive, send):
    """Точка входа для ASGI приложения."""
    if scope["type"] in {"http", "lifespan"}:
        await django_application(scope, receive, send)
    else:
        raise NotImplementedError(f"Unknown scope type {scope['type']}")
