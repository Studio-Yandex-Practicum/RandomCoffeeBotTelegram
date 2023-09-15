from pathlib import Path

import environ
from dotenv import find_dotenv


DEBUG = True

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
if DEBUG := env.bool("DEBUG", default=True):
    environ.Env.read_env(find_dotenv(".env", raise_error_if_not_found=True))

SECRET_KEY = env.str('SECRET_KEY')

env.list('ALLOWED_HOSTS', default=['*'])

DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LOCAL_APPS = [
    'bot',
    'admin_user'
]

EXTERNAL_APPS = [

]

INSTALLED_APPS = DEFAULT_APPS + LOCAL_APPS + EXTERNAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'

TELEGRAM_TOKEN = env.str('TELEGRAM_TOKEN')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

WEBHOOK_MODE = False
WEBHOOK_URL = ''
WEBHOOK_SECRET_KEY = ''

PERSISTANCE_DIR = BASE_DIR / 'persistance_data'
PERSISTANCE_PATH = PERSISTANCE_DIR / 'persistance_file'

Path.mkdir(PERSISTANCE_DIR, exist_ok=True)
