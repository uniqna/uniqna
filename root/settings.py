import os
from django.conf.global_settings import TEMPLATES

try:
    from root import secret_settings
except ImportError:
    pass

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
PREPEND_WWW = True
SITE_ID = 2
STATIC_URL = '/static/'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'home',
    'post',
    'RestApi',
    'search',
    'threads',
    'user',
    'django_bleach',
    'django_user_agents',
    'el_pagination',
    'mptt',
    'rest_framework',
    'robots',
    'widget_tweaks',
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': 60,
        'LOCATION': 'default-location',
    }
}

USER_AGENTS_CACHE = 'default'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'root.middleware.UserAgentMiddleware',
    'root.middleware.DebugMiddleware'
]

ROOT_URLCONF = 'root.urls'

TEMPLATES += [
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

TEMPLATES[0]['OPTIONS']['context_processors'].insert(
    0, 'django.template.context_processors.request')

WSGI_APPLICATION = 'root.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
    STATIC_ROOT = os.path.join(BASE_DIR, "..", "www", "static")
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'uniqna',
            'USER': 'moderator',
            'PASSWORD': 'password',
            'HOST': 'localhost',
            'PORT': '',
        }
    }
    DEBUG = True
    # STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False
    PREPEND_WWW = False


# Mailing
if 'SECRET_KEY' in os.environ:
    SECRET_KEY = os.environ['SECRET_KEY']
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_SSL = True
    EMAIL_HOST = os.environ['EMAIL_HOST']
    EMAIL_PORT = os.environ['EMAIL_PORT']
    EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
    DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']
    SERVER_EMAIL = os.environ['SERVER_EMAIL']
else:
    SECRET_KEY = secret_settings.SECRET_KEY
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_SSL = True
    EMAIL_HOST = secret_settings.EMAIL_HOST
    EMAIL_PORT = secret_settings.EMAIL_PORT
    EMAIL_HOST_USER = secret_settings.EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD = secret_settings.EMAIL_HOST_PASSWORD
    DEFAULT_FROM_EMAIL = secret_settings.DEFAULT_FROM_EMAIL
    SERVER_EMAIL = secret_settings.SERVER_EMAIL
    MG_KEY = secret_settings.MG_KEY
    MG_URL = secret_settings.MG_URL
    MG_FROM = secret_settings.MG_FROM

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TIME_ZONE = 'Asia/Kolkata'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

# Bleach
BLEACH_ALLOWED_TAGS = ['p', 'h3', 'h4', 'em', 'strong', 'a', 'ul', 'ol', 'li',
                       'blockquote', 'code', 'table', 'thead', 'tbody', 'td',
                       'th', 'tr', 'pre', 'img', 'b', 'br']
BLEACH_ALLOWED_ATTRIBUTES = ['href', 'title', 'name', 'align', 'width', 'src']
BLEACH_STRIP_TAGS = True

# Pagination
EL_PAGINATION_NEXT_LABEL = """<button class="mdl-button mdl-js-button mdl-button--accent mdl-js-ripple-effect">Load More</button>"""
