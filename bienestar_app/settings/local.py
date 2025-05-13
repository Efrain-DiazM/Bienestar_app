from .base import *
from decouple import config
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", "False") == "True"

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

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
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', 'localhost'),  # Valor predeterminado: localhost
        'PORT': config('DB_PORT', '3306'),       # Valor predeterminado: 3306
        'OPTIONS': {
             'ssl': os.path.join(BASE_DIR, 'cert', 'BaltimoreCyberTrustRoot.crt.pem'),  # para Azure
         },
    }
}

# DATABASES = {
#     'default': dj_database_url.config(default=os.getenv("DATABASE_URL"))
# }

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
