
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY=os.environ.get('SECRET_KEY')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'djangoicin2@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL="djangoicin2@gmail.com"

MANAGERS=(
    ("Mustafa Dalga","djangoicin2@gmail.com"),
)
ADMINS=MANAGERS

ALLOWED_HOSTS = [".herokuapp.com"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party
    'storages',

    # Our apps
    'products',
    'accounts',
    'analytics',
    'addresses',
    'billing',
    'orders',
    'marketing',
    'search',
    'tags',
    'carts',
]

AUTH_USER_MODEL="accounts.User"  #changes the builin user model to ours




MAILCHIP_API_KEY=os.environ.get("MAILCHIP_API_KEY")
MAILCHIP_DATA_CENTER="us20"
MAILCHIP_EMAIL_LIST_ID=os.environ.get("MAILCHIP_EMAIL_LIST_ID")

FORCE_SESSION_TO_ONE = False
FORCE_INACTIVE_USER_ENDSESSION= False
STRIPE_SECRET_KEY=os.environ.get("STRIPE_SECRET_KEY","sk_test_53qdSBhMf6DpdVhkomQzAkSD00t9IcQotu")
STRIPE_PUB_KEY=os.environ.get("STRIPE_PUB_KEY","pk_test_5wkb1M4U4Z0WN44BcoH2XnXJ00pa2DsSqv")

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

LOGOUT_REDIRECT_URL="/login/"
ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'ecommerce.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

import dj_database_url
db_from_env = dj_database_url.config() # postgresql database in heroku
DATABASES['default'].update(db_from_env)
DATABASES['default']['CONN_MAX_AGE'] = 500



# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT=os.path.join(BASE_DIR, 'static', 'static_root')
STATIC_URL = '/static/'
STATICFILES_DIRS=[
    os.path.join(BASE_DIR, 'ecommerce/static')
]
MEDIA_URL = '/media/'
MEDIA_ROOT=os.path.join(BASE_DIR, "static", 'media_root')


from ecommerce.aws.conf import *

CORS_REPLACE_HTTPS_REFERER      = True
HOST_SCHEME                     = "https://"
SECURE_PROXY_SSL_HEADER         = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT             = True
SESSION_COOKIE_SECURE           = True
CSRF_COOKIE_SECURE              = True
SECURE_HSTS_INCLUDE_SUBDOMAINS  = True
SECURE_HSTS_SECONDS             = 1000000
SECURE_FRAME_DENY               = True



