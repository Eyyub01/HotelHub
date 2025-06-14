import os

from pathlib import Path
from datetime import timedelta

import dj_database_url

from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

AUTH_USER_MODEL = 'accounts.CustomUser'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')


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
    'django.middleware.csrf.CsrfViewMiddleware',
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

# Redis Configuration
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
REDIS_DB = os.getenv('REDIS_DB', 0)
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', 'redis_password')

REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
if REDIS_PASSWORD:
    REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

# Celery settings
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', REDIS_URL)
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', REDIS_URL)
CELERY_TIMEZONE = os.getenv('CELERY_TIMEZONE', 'Asia/Baku')
CELERY_TASK_TRACK_STARTED = os.getenv('CELERY_TASK_TRACK_STARTED', 'True').lower() == 'true'
CELERY_TASK_TIME_LIMIT = int(os.getenv('CELERY_TASK_TIME_LIMIT', 1800))

# Channel layers configuration
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_URL],
        },
    },
}

# Cache configuration
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_CONNECT_TIMEOUT": 5,
            "SOCKET_TIMEOUT": 5,
            "RETRY_ON_TIMEOUT": True,
            "MAX_CONNECTIONS": 1000,
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
        }
    }
}

# Session configuration
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# Database configuration
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL', 'postgres://postgres:postgres@db:5432/postgres'),
        conn_max_age=600
    )
}

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# OpenAI configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

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

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_CACHE_BACKEND = 'redis://localhost:6379' 

#Logging settings
LOGGING_DIR = os.path.join(BASE_DIR, 'logging')
os.makedirs(LOGGING_DIR, exist_ok=True)

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

CACHE_TIMEOUT = 60*5

#Elasticsearch settings

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'http://elasticsearch:9200'
    },
}
