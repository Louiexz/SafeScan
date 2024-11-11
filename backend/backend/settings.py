from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", default=False)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv(), default="127.0.0.1")

# Application definition

MY_APPS = [
    "safescan.apps.SafeScanConfig",
]
THIRD_APPS = [
    'rest_framework',
    'django_vite',
    'corsheaders',
    'rest_framework.authtoken',
    'django_extensions',
]
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
] + MY_APPS + THIRD_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
CORS_ALLOW_CREDENTIALS = True
CSRF_COOKIE_HTTPONLY = False  # Permite o acesso ao CSRF cookie por JavaScript
CSRF_COOKIE_NAME = "csrftoken"  # O nome do cookie CSRF, que será acessado pelo frontend

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:8000",
]
CORS_ORIGINS_WHITELIST = [
    "http://localhost:5173",
    "http://127.0.0.1:8000",
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'origin',
    'x-csrftoken',
]
SESSION_COOKIE_AGE = 1800
SESSION_COOKIE_SAMESITE = 'None'  # Permite o envio de cookies em requisições cross-origin
SESSION_COOKIE_SECURE = True  # Garante que o cookie só será enviado sobre HTTPS

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

ROOT_URLCONF = 'backend.urls'
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
}
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

WSGI_APPLICATION = 'backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'safescan/static',  # Diretório onde os arquivos do Vite serão gerados para desenvolvimento
]

# Defina o STATIC_ROOT para produção
STATIC_ROOT = BASE_DIR / 'safescan/static/.vite/'  # Local onde 'collectstatic' colocará os arquivos em produção 'django.db.models.BigAutoField'

VITE_MANIFEST_PATH = BASE_DIR / '/static/'
VITE_APP_DIR = BASE_DIR.parent / 'frontend'          # Diretório onde o Vite está configurado (frontend)
VITE_DEV_MODE = DEBUG                          # Ativa o modo de desenvolvimento do Vite quando DEBUG está True
VITE_STATIC_ROOT = BASE_DIR / 'safescan/static'     # Diretório onde o Vite deve colocar os arquivos em produção

if VITE_APP_DIR is None or not VITE_APP_DIR.exists():
    raise ValueError("VITE_APP_DIR não está configurado corretamente.")
    
if VITE_STATIC_ROOT is None or not VITE_STATIC_ROOT.exists():
    raise ValueError("VITE_STATIC_ROOT não está configurado corretamente.")