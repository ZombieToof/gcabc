"""
Django settings for gcsite project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i1*nuyyz#&cry2341chy-%hgj=6+3qv0z-==!s(@+z!#%d4n=h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'gcsite/templates'),)
INTERNAL_IPS = ['127.0.0.1',  # django debug toolbar
                '10.0.2.2']   # Vagrant host

ALLOWED_HOSTS = []


REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'debug_toolbar.apps.DebugToolbarConfig',  # Django >= 1.7
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django_phpBB3',
#    'rest_framework',
    'abcapp',
    'pinax_theme_bootstrap',
    'bootstrapform',
#    'django_pdb',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'abcapp.middleware.phpbb.PhpbbAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'abcapp.middleware.cache.RequestCacheMiddleware',
#    'django_pdb.middleware.PdbMiddleware',  # has to be the last middleware
    )

ROOT_URLCONF = 'gcsite.urls'

WSGI_APPLICATION = 'gcsite.wsgi.application'


#------------------------------------------------------------------------------
# django-phpBB3 settings:

PHPBB_TABLE_PREFIX = u"phpbb_"

PHPBB_CAPTCHA_QUESTIONS_MODEL_EXIST = False

# Add PhpBBPasswordHasher to the default hashers
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
    'django_phpBB3.hashers.PhpBB3PasswordHasher',
)

#------------------------------------------------------------------------------


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'phpbb',
        'USER': 'phpbb',
        'PASSWORD': 'phpbb',
    }
}

# import sys
# if 'test' in sys.argv:
#     DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
#     DATABASES['default']['NAME'] = 'testdatabase.db3'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "gcsite/static"),)
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "abcapp.static.NpmFreeAppDirectoriesFinder")
