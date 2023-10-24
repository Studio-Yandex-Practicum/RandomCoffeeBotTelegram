import os
from pathlib import Path

import environ
from dotenv import find_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ROOT_DIR = BASE_DIR.parent

env = environ.Env()

if DEBUG := env.bool("DEBUG", default=True):
    environ.Env.read_env(find_dotenv(".env"))

DEFAULT = 'some_default_key'

SECRET_KEY = env.str('SECRET_KEY', default=DEFAULT)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])

AUTH_USER_MODEL = "admin_user.AdminUser"

DEFAULT_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

LOCAL_APPS = ["bot", "admin_user", ]

EXTERNAL_APPS = ["admin_interface", "colorfield"]

INSTALLED_APPS = EXTERNAL_APPS + DEFAULT_APPS + LOCAL_APPS

X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": env.str("POSTGRES_ENGINE", default='django.db.backends.postgresql'),
        "NAME": env.str("POSTGRES_NAME", default='postgres'),
        "USER": env.str("POSTGRES_USER", default='postgres'),
        "PASSWORD": env.str("POSTGRES_PASSWORD", default='postgres'),
        "HOST": env.str("POSTGRES_HOST", default='localhost'),
        "PORT": env.str("POSTGRES_PORT", default='5432'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

REDIS = {
    'host': env.str('REDIS_HOST', default='localhost'),
    'port': env.str('REDIS_PORT', default='6379')
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(ROOT_DIR, 'static/')

TELEGRAM_TOKEN = env.str('TELEGRAM_TOKEN', default=DEFAULT)
USE_REDIS_PERSISTENCE = env.bool('REDIS', default=False)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

WEBHOOK_MODE = False
WEBHOOK_URL = ""
WEBHOOK_SECRET_KEY = ""

PERSISTENCE_DIR = ROOT_DIR / "persistence_data"
PERSISTENCE_PATH = PERSISTENCE_DIR / "persistence_file"

Path.mkdir(PERSISTENCE_DIR, exist_ok=True)

# Настройки пагинации

DEFAULT_PAGE_NUMBER = 5 # Количество страниц в панели пагинации по умолчанию
KEYBOARD_PAGE_OFFSET = 3 # Сдвиг страниц, если количество превышает DEFAULT_PAGE_NUMBER
PROFESSION_PER_PAGE = 5 # Количество профессий на странице
PAGE_SEP_SYMBOL = "#" # Символ, отделяющий номер страницы
DEFAULT_PAGE = 1 # Номер страницы по умолчанию

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST = env.str("EMAIL_HOST", default="smtp.yandex.ru")
try:
    EMAIL_PORT = env.int("EMAIL_PORT", default=465)
except ValueError:
    EMAIL_PORT = 465
EMAIL_HOST_USER = env.str("EMAIL_ACCOUNT", default="example@yandex.ru")
EMAIL_HOST_PASSWORD = env.str("EMAIL_PASSWORD", default="password")
EMAIL_TIMEOUT = 5
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
DEFAULT_RECEIVER = env.str("DEFAULT_EMAIL_ADDRESS", default="NOT_SET")
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
