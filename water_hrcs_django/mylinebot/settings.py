
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

EMAIL_HOST      = 'smtp.gmail.com'
EMAIL_HOST_PASSWORD = os.getenv("MAILPASS"),
EMAIL_HOST_USER = 'cgptiot@gmail.com'
EMAIL_PORT      = 25
EMAIL_USE_TLS = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL  = 'cgptiot@gmail.com'





# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ptt0oq10wusdvstr5yk%o80p59kh@z)xxs^)yhgh3=g!hw*x(9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = [
    'water-hrcs-django.azurewebsites.net',
    '127.0.0.1',# 允許的網域名稱
    '*'
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

# 新建立的Django應用程式(APP)
    'clockInlinebot.apps.ClockinlinebotConfig',
    'corsheaders',
    'rest_framework',
    'drf_yasg',
    'HRCS',
    "whitenoise.runserver_nostatic"

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'

]
AUTHENTICATION_BACKENDS = ['HRCS.passbackend.PasswordBackend']

ROOT_URLCONF = 'mylinebot.urls'
CORS_ALLOW_ALL_ORIGINS=True
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "token",
]




TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [Path(BASE_DIR, 'clockInlinebot/templates')],
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

WSGI_APPLICATION = 'mylinebot.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'water_hrcs',
        'USER': 'water_hrcs',
        'PASSWORD': os.getenv("DBPASS"),
        'HOST': 'cgpt-mysql.mysql.database.azure.com',
        'PORT': '3306',
        'OPTIONS': {
            'ssl': {'ca': '', },
        },
    },

}









# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-Hant'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = False

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATICFILES_STORAGE = ('whitenoise.storage.CompressedManifestStaticFilesStorage')
STATIC_URL = os.environ.get("DJANGO_STATIC_URL", "/clockInlinebot/static/")
STATIC_ROOT = os.environ.get("DJANGO_STATIC_ROOT", "./clockInlinebot/static/")

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# LINE Developers上所取得的兩個憑證設定，來與LINE頻道(Channel)進行連結
# LINE_CHANNEL_ACCESS_TOKEN = 'TQrz3++rf46Ff3R6vvzcdPmVOs63aCwqX6vs5lEQxgYQaeWA3eIo/vLUhKiA7/+7mlsFlNI/Sxl/mi1VL0jMzgK010e77L6aKcNxU8i1a/AAdbYL3ApMMTJ/hpyrb11AW/lkJebdk/LI7NWOCk59ygdB04t89/1O/w1cDnyilFU='
# LINE_CHANNEL_SECRET = '1bc5cbac2b63d2aaf0c5894c3cd615cd'

LINE_CHANNEL_ACCESS_TOKEN = 'CpLBe4eDOxtYKlZCOQluSroTi99uDCZRHkWUvbomQqYmxp7Qq3J4Jq/VYDPE0ZYiCH/oa9lOG2LC+l0feXgp1Uk0zFqoOaCMHmgYBX1NcCFnS7fa8Ijvr4nJRjjBaA1GhlYsLQVOmyIVbnP+5rJrZgdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = '003b0be48e2a1d2311405799c3e7fcbf'
