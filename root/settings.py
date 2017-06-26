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

ALLOWED_HOSTS = ['.uniqna.com', '.localhost']
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
PREPEND_WWW = True
SITE_ID = 1
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


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
    'api',
    'search',
    'threads',
    'user',
    'django_bleach',
    'el_pagination',
    'mptt',
    'pipeline',
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


if 'SECRET_KEY' in os.environ:
    SECRET_KEY = os.environ['SECRET_KEY']
    MG_KEY = os.environ['MG_KEY']
    MG_URL = os.environ['MG_URL']
    MG_FROM = os.environ['SECRET_KEY']
else:
    SECRET_KEY = secret_settings.SECRET_KEY
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
BLEACH_ALLOWED_TAGS = ['p', 'h3', 'h4', 'strong', 'a', 'ul', 'ol', 'li',
                       'blockquote', 'code', 'table', 'thead', 'tbody', 'td',
                       'th', 'tr', 'pre', 'img', 'br']
BLEACH_ALLOWED_ATTRIBUTES = ['href', 'title', 'name', 'align', 'width', 'src']

# Pipeline
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

PIPELINE = {
    'STYLESHEETS': {
        'base': {
            'source_filenames': (
              'css/bulma.css',
              'css/base.css',
              'css/navbar.css',
            ),
            'output_filename': 'base.css',
        },
        'home': {
            'source_filenames': (
              'css/twemoji-awesome.css',
              'css/question.css',
            ),
            'output_filename': 'home.css',
        },
        'new': {
            'source_filenames': (
              'css/new.css',
            ),
            'output_filename': 'new.css',
        },
        'thread': {
            'source_filenames': (
              'css/thread.css',
              'css/thread_author_panel.css',
            ),
            'output_filename': 'thread.css',
        },
        'profile': {
            'source_filenames': (
              'css/profile.css',
              'css/question.css',
              'css/answer.css',
            ),
            'output_filename': 'profile.css',
        },
        'channel': {
            'source_filenames': (
              'css/channel.css',
              'css/question.css',
            ),
            'output_filename': 'channel.css',
        },
        'register': {
            'source_filenames': (
              'css/register.css',
              'css/question.css',
            ),
            'output_filename': 'register.css',
        },
        'forgot': {
            'source_filenames': (
              'css/forgot.css',
            ),
            'output_filename': 'forgot.css',
        },
        'notifications': {
            'source_filenames': (
              'css/notifications.css',
            ),
            'output_filename': 'notifications.css',
        },
    },
    'JAVASCRIPT': {
        'base': {
            'source_filenames': (
              'js/base.js',
              'js/vue.js'
            ),
            'output_filename': 'base.js',
        },
        'home': {
            'source_filenames': (
              'js/vote.js',
            ),
            'output_filename': 'home.js',
        },
        'new': {
            'source_filenames': (
              'js/submit.js',
              'js/notif_delete.js'
            ),
            'output_filename': 'new.js',
        },
        'thread': {
            'source_filenames': (
              'js/vote.js',
              'js/thread_author_panel.js',
              'js/notif_delete.js',
              'js/submit.js',
              'js/contribute.js',
              'js/reply_modal.js',
            ),
            'output_filename': 'thread.js',
        },
        'profile': {
            'source_filenames': (
              'js/vote.js',
              'js/notif_delete.js',
              'js/submit.js',
              'js/profile.js',
            ),
            'output_filename': 'profile.js',
        },
        'channel': {
            'source_filenames': (
              'js/vote.js',
            ),
            'output_filename': 'channel.js',
        },
        'register': {
            'source_filenames': (
              'js/submit.js',
              'js/notif_delete.js'
            ),
            'output_filename': 'register.js',
        },
        'forgot': {
            'source_filenames': (
              'js/submit.js',
              'js/notif_delete.js'
            ),
            'output_filename': 'forgot.js',
        },
    }
}
