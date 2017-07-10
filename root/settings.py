import os

import raven
from django.conf.global_settings import TEMPLATES

try:
    from root import secret_settings
except ImportError:
    pass

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_ID = 1
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
DEBUG = False

if os.environ.get('DEBUG'):
    DEBUG = True

if os.environ.get('PRODUCTION'):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MG_KEY = os.environ.get('MG_KEY')
    MG_URL = os.environ.get('MG_URL')
    MG_FROM = os.environ.get('MG_FROM')
    ALLOWED_HOSTS = ['.uniqna.com']
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    PREPEND_WWW = True
else:
    SECRET_KEY = secret_settings.SECRET_KEY
    MG_KEY = secret_settings.MG_KEY
    MG_URL = secret_settings.MG_URL
    MG_FROM = secret_settings.MG_FROM
    ALLOWED_HOSTS = ['*']

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# Manual debug override for generating static files
# DEBUG = False

if 'TRAVIS' in os.environ or DEBUG:
    PREPEND_WWW = False
    ALLOWED_HOSTS = ['*']
    STATICFILES_STORAGE = 'pipeline.storage.NonPackagingPipelineStorage'


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
    'raven.contrib.django.raven_compat',
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
if os.environ.get('PRODUCTION'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'uniqna',
            'USER': 'moderator',
            'PASSWORD': os.environ.get('DB_PASSWORD'),
            'HOST': 'localhost',
            'PORT': '',
        }
    }
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
BLEACH_ALLOWED_TAGS = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'a', 'ul', 'ol', 'li',
                       'blockquote', 'code', 'table', 'thead', 'tbody', 'td',
                       'th', 'tr', 'pre', 'br', 'em', 'b']
BLEACH_ALLOWED_ATTRIBUTES = ['href', 'title', 'name', 'align', 'width']

# Pipeline
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
        'login': {
            'source_filenames': (
                'css/bulma.css',
                'css/twemoji-awesome.css',
                'css/question.css',
                'css/login.css',
            ),
            'output_filename': 'login.css',
        },
        'home': {
            'source_filenames': (
                'css/twemoji-awesome.css',
                'css/question.css',
                'css/vote.css',
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
                'css/answer.css',
                'css/vote.css',
                'css/tada.css',
            ),
            'output_filename': 'thread.css',
        },
        'profile': {
            'source_filenames': (
                'css/profile.css',
                'css/question.css',
                'css/answer.css',
                'css/vote.css',
            ),
            'output_filename': 'profile.css',
        },
        'channel': {
            'source_filenames': (
                'css/channel.css',
                'css/question.css',
                'css/vote.css',
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
                'js/third_party/vue.min.js',
                'js/third_party/jquery.min.js',
                'js/base.js',
            ),
            'output_filename': 'js/base.js',
        },
        'login': {
            'source_filenames': (
                'js/third_party/vue.min.js',
                'js/third_party/jquery.min.js',
                'js/notif_delete.js',
                'js/submit.js',
            ),
            'output_filename': 'js/login.js',
        },
        'home': {
            'source_filenames': (
                'js/infinite_scroll.js',
                'js/frontpage.js',
                'js/vote.js',
            ),
            'output_filename': 'js/home.js',
        },
        'new': {
            'source_filenames': (
                'js/submit.js',
                'js/notif_delete.js'
            ),
            'output_filename': 'js/new.js',
        },
        'thread': {
            'source_filenames': (
                'js/vote.js',
                'js/thread_author_panel.js',
                'js/notif_delete.js',
                'js/submit.js',
                'js/contribute.js',
                'js/reply_modal.js',
                'js/collapse.js',
                'js/third_party/clipboard.min.js',
                'js/permalink.js',
            ),
            'output_filename': 'js/thread.js',
        },
        'profile': {
            'source_filenames': (
                'js/vote.js',
                'js/notif_delete.js',
                'js/submit.js',
                'js/profile.js',
            ),
            'output_filename': 'js/profile.js',
        },
        'channel': {
            'source_filenames': (
                'js/vote.js',
            ),
            'output_filename': 'js/channel.js',
        },
        'register': {
            'source_filenames': (
                'js/submit.js',
                'js/notif_delete.js',
                'js/register.js',
            ),
            'output_filename': 'js/register.js',
        },
        'usermanage': {
            'source_filenames': (
                'js/attach_csrf_header.js',
                'js/submit.js',
                'js/notif_delete.js',
                'js/manage.js',
            ),
            'output_filename': 'js/usermanage.js',
        },
        'forgot': {
            'source_filenames': (
                'js/submit.js',
                'js/notif_delete.js'
            ),
            'output_filename': 'js/forgot.js',
        },
    }
}

PIPELINE['CSS_COMPRESSOR'] = 'pipeline.compressors.cssmin.CSSMinCompressor'
PIPELINE['JS_COMPRESSOR'] = 'pipeline.compressors.uglifyjs.UglifyJSCompressor'

# Sentry
RAVEN_CONFIG = {
    'dsn': 'https://cf76b80a140646d18c0340c614decf62:e8a22e4ed77148afb77c6cfdea8cb482@sentry.io/186841',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
}
