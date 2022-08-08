from split_settings.tools import include
from dotenv import load_dotenv
load_dotenv() 

include(
    'components/auth_password_validators.py',
    'components/database.py',
    'components/installed_apps.py',
    'components/middleware.py',
    'components/tempates.py',
) 

from pathlib import Path
import os

DEBUG = os.environ.get('DEBUG', False) == 'True'
ALLOWED_HOSTS = ['127.0.0.1'] 


BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-zemvma(i#(znnxfs_@o%+5(540z)^o(liq5w!t@y%60w2m3507'
ROOT_URLCONF = 'kino.urls'
WSGI_APPLICATION = 'kino.wsgi.application'

LANGUAGE_CODE = 'ru-RU'
LOCALE_PATHS = ['movies/locale'] 
TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#this is for debuger
INTERNAL_IPS = [
    "127.0.0.1",
]