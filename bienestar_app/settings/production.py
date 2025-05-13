from .base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG =  os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', default='').split(',')

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'bienestar_db',
#         'USER': 'adminhbu',
#         'PASSWORD': 'N0m4m35.',
#         'HOST': 'bienestarhbu.mysql.database.azure.com',
#         'PORT': '3306',
#         'OPTIONS': {
#             'ssl': {'ca': '/cert/BaltimoreCyberTrustRoot.crt.pem'},  # para Azure
#         },
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),      # puerto por defecto
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET NAMES 'utf8mb4' COLLATE 'utf8mb4_unicode_ci'"
        },
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'