from pathlib import Path
from datetime import timedelta
import os
import logging

logger = logging.getLogger(__name__)

# Configurações logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.StreamHandler()]
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', '')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'false').lower() in ('1', 'true', 'yes', 'y')

if DEBUG:
    ALLOWED_HOSTS = ['*', ]
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:5173",     # para Vite no dev local
        "http://127.0.0.1:5173",     # alternativa de acesso local
        "http://192.168.1.104:5173",
        "http://192.168.1.100"
    ]
    CSRF_TRUSTED_ORIGINS = [
        "http://192.168.1.100",
        "http://localhost:8001",
        "http://127.0.0.1:8001",
        "https://blogapi.leonoliveira.com.br"
    ]
else:
    ALLOWED_HOSTS = [
        "blogapi.leonoliveira.com.br"
    ]
    CORS_ALLOWED_ORIGINS = [
        "https://leonoliveira.com.br"
    ]

    CSRF_TRUSTED_ORIGINS = [
        "https://blogapi.leonoliveira.com.br"
    ]

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'channels',
    'corsheaders',
    'drf_yasg',
    'api'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'chat.urls'

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

WSGI_APPLICATION = 'chat.wsgi.application'

ASGI_APPLICATION = 'terminal.asgi.application' # Para Websocket


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

required_vars = ['PSQL_HOST', 'PSQL_PORT', 'PSQL_USER', 'PSQL_PASS', 'PSQL_DB']

missing_vars = [var for var in required_vars if var not in os.environ]

if not missing_vars:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('PSQL_DB'),
            'USER': os.environ.get('PSQL_USER'),
            'PASSWORD': os.environ.get('PSQL_PASS'),
            'HOST': os.environ.get('PSQL_HOST'),
            'PORT': os.environ.get('PSQL_PORT', '5432'),
        }
    }

    logger.info(
        f"Conectado ao Banco {os.environ.get('PSQL_HOST')}:{os.environ.get('PSQL_PORT')}"
    )
else:
    logger.warning(
        f"As seguintes variáveis de ambiente estão ausentes: {', '.join(missing_vars)}\n"
        f"Configure as variáveis de ambiente antes de continuar."
    )

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_ROOT = 'staticfiles'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_AUTHENTICATION_CLASSES': [
 'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=120),  # Duração do token
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),     # Duração do refresh token
}

SWAGGER_SETTINGS = {
    'LOGIN_URL': '/admin/login/',
    'LOGOUT_URL': '/admin/logout/',
    'DOC_EXPANSION': 'none',
    'DEFAULT_MODEL_RENDERING': 'exemple',
    'VALIDATOR_URL': None
}

URL_API = os.environ.get('URL_API', 'http://127.0.0.1:8001')

URL_REDIS = os.environ.get('URL_REDIS', '127.0.0.1')
PORT_REDIS = os.environ.get('PORT_REDIS', 6379)

# Channels websocket broker (REDIS)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(URL_REDIS, PORT_REDIS)],  # Or your Redis host/port
        },
    },
}
