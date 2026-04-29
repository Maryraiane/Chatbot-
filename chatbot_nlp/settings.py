from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# 🔐 SEGURANÇA
# =========================

SECRET_KEY = os.getenv("SECRET_KEY", "chave-local")

DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", ".onrender.com").split(",")


# =========================
# 📦 APPS
# =========================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'chat',
]


# =========================
# ⚙️ MIDDLEWARE
# =========================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# =========================
# 🌐 URLs
# =========================

ROOT_URLCONF = 'chatbot_nlp.urls'


# =========================
# 🧩 TEMPLATES
# =========================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# =========================
# 🚀 WSGI
# =========================

WSGI_APPLICATION = 'chatbot_nlp.wsgi.application'


# =========================
# 🗄️ BANCO
# =========================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# =========================
# 🌍 INTERNACIONALIZAÇÃO
# =========================

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True
USE_TZ = True


# =========================
# 📁 STATIC FILES
# =========================

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# pasta opcional para arquivos estáticos locais
STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# =========================
# 🔒 SEGURANÇA EXTRA
# =========================

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True


# =========================
# 📝 LOGGING (console)
# =========================

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}


# =========================
# 🔢 DEFAULT
# =========================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'