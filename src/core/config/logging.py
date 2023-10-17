import sys

from loguru import logger


def setup_logger():
    """Функция для настройки логгера."""
    logger.remove(0)
    logger.add(
        sys.stdout, level="DEBUG", enqueue=True, backtrace=True, diagnose=True
    )
    logger.add(
        "../logs/{time:YYYY-MM-DD}.log",
        rotation="1 month",
        level="INFO",
        enqueue=True,
        backtrace=True,
        diagnose=True,
    )


def log_function(func):
    """Декоратор для логирования обработчиков и шедулеров."""
    schedulers_data = [
        "send_is_pair_successful_message",
    ]

    async def wrapper(*args, **kwargs):
        if func.__name__ in schedulers_data:
            context = args[0] if args else kwargs.get("context")
            job = context.job if context else None
            user = job.data if job else None
            func_type = "Scheduler"
        else:
            update = args[0] if args else kwargs.get("update")
            user = update.effective_user if update else None
            func_type = "Handler"
        user_id = user.id if user else "Unknown"
        username = user.username if user else "Unknown"
        try:
            result = await func(*args, **kwargs)
            logger.info(
                f"User: {username} (ID: {user_id}) | "
                f"{func_type}: {func.__name__}"
            )
            return result
        except Exception as e:
            logger.exception(
                f"User: {username} "
                f"(ID: {user_id}) | "
                f"{func_type}: {func.__name__} | "
                f"Exception: {e}"
            )
            raise e

    return wrapper
