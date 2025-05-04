import os

from pathlib import Path
from datetime import timedelta

from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

AUTH_USER_MODEL = 'accounts.CustomUser'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-*#jt63c2$!ytn6u3a14&$er^fwnqk*8_mm$8poc-ne6k7$_axh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Django Apps
    'hotels',
    'accounts',
    'rooms',
    'bookings',
    'favorites',
    'chat',
    'ai',

    # Third-party apps
    'rest_framework',
    'drf_spectacular',
    'django_countries',
    'django_filters',
    'django_celery_beat',
    'rest_framework_simplejwt',
    'django_redis',
    'django_elasticsearch_dsl',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100
}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'hotelhub.middlewares.logging.RequestLoggingMiddleware',
]

SPECTACULAR_SETTINGS = {
    'TITLE': 'HotelHub API',
    'DESCRIPTION': 'Simple API for your Hotels',
    'VERSION': '0.1.2',
    'SERVE_INCLUDE_SCHEMA': False,
}

ROOT_URLCONF = 'hotelhub.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ASGI_APPLICATION = 'hotelhub.asgi.application'
WSGI_APPLICATION = 'hotelhub.wsgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),  
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',  
    'SIGNING_KEY': SECRET_KEY, 
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',), 
    'USER_ID_FIELD': 'id',  
    'USER_ID_CLAIM': 'user_id', 
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
}
# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Baku'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Celery settings
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')  
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'

#Logging settings
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {asctime} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        # App-specific log files
        "accounts_file": {
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logging/accounts.log"),
            "formatter": "verbose",
        },
        "hotels_file": {
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logging/hotels.log"),
            "formatter": "verbose",
        },
        "rooms_file": {
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logging/rooms.log"),
            "formatter": "verbose",
        },
        "bookings_file": {
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logging/bookings.log"),
            "formatter": "verbose",
        },
        "favorites_file": {
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logging/favorites.log"),
            "formatter": "verbose",
        },
        "chat_file": {
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logging/chat.log"),
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
        # App-specific loggers
        "accounts": {
            "handlers": ["accounts_file"],
            "level": "INFO",
            "propagate": False,
        },
        "hotels": {
            "handlers": ["hotels_file"],
            "level": "INFO",
            "propagate": False,
        },
        "rooms": {
            "handlers": ["rooms_file"],
            "level": "INFO",
            "propagate": False,
        },
        "bookings": {
            "handlers": ["bookings_file"],
            "level": "INFO",
            "propagate": False,
        },
        "favorites": {
            "handlers": ["favorites_file"],
            "level": "INFO",
            "propagate": False,
        },
        "chat": {
            "handlers": ["chat_file"],
            "level": "INFO",
            "propagate": False,
        },
        "ai": {
            "handlers": ["chat_file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

#Mail settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'abbaszadeeyyub@gmail.com'  
EMAIL_HOST_PASSWORD = 'boct xmvn eifl sltf' 

# Cache settings
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('REDIS_URL', 'redis://redis:6379/1'),  
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
CACHE_TIMEOUT = 60*5

#Elasticsearch settings

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'http://elasticsearch:9200'
    },
}