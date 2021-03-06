"""
Django settings for write_space project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import environ

env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATICFILES_DIRS=[os.path.join(BASE_DIR,"static")]
TEMPLATE_DIR=os.path.join(BASE_DIR,"templates")
MEDIA_DIR = os.path.join(BASE_DIR,"media")
STATIC_DIR=os.path.join(BASE_DIR,"admin_static")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$7-2w&_j^(fs7j&&@*^jb&0+_o*cel7lx1ub92tvw8%im#xn=i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "rest_framework",
    "mptt",
    "widget_tweaks",
    # "crispy_forms",
    # "ckeditor",
    # "ckeditor_uploader",
    "accounts",
    "posts",
    "django_summernote",
    "cloudinary",
]
# CRISPY_TEMPLATE_PACK = 'bootstrap3'
# CKEDITOR_UPLOAD_PATH = "uploads/"
import cloudinary

cloudinary.config(
cloud_name = env('CLOUD_NAME'),
api_key = env('API_KEY'),
api_secret = env('API_SECRET')
)



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'write_space.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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

WSGI_APPLICATION = 'write_space.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = STATIC_DIR

LOGIN_REDIRECT_URL="/accounts/first_step/"
LOGOUT_REDIRECT_URL="/"

MEDIA_ROOT = MEDIA_DIR
MEDIA_URL = "/media/"


REST_FRAMEWORK = {
"DEFAULT_RENDERER_CLASSES":(
"rest_framework.renderers.JSONRenderer",
"rest_framework.renderers.BrowsableAPIRenderer",
),
# "DEFAULT_PARSER_CLASSES":(
# "rest_framework.parsers.JSONParser",
# ),

'DEFAULT_PERMISSION_CLASSES': (
    'rest_framework.permissions.IsAuthenticated',
),
'DEFAULT_AUTHENTICATION_CLASSES': (
    # 'rest_framework.authentication.TokenAuthentication',
    'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    'rest_framework.authentication.SessionAuthentication',
    'rest_framework.authentication.BasicAuthentication',
),
}

JWT_AUTH = {
    'JWT_ALLOW_REFRESH': True,
}

SUMMERNOTE_CONFIG = {

 # You can put custom Summernote settings
    'summernote': {
        # Change editor size
        'width': '100%',
        'height': '480',

        # Toolbar customization
        # https://summernote.org/deep-dive/#custom-toolbar-popover
        'toolbar': [
            ['style', ['style']],
            ['font', ['bold', 'underline', 'clear']],
            ['fontname', ['fontname']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['table', ['table']],
            ['insert', ['emoji','link', 'picture', 'video']]
        ]
    },
"css":("/static/write_space/css/summernote_plugin.css",),
"js":("/static/write_space/js/summernote_plugin.js",)
}
