# Ficheiro de configurações principais do Django.

import os
from pathlib import Path

# Construa caminhos relativos ao diretório-base.
BASE_DIR = Path(__file__).resolve().parent.parent

# Chave secreta para uso em produção
SECRET_KEY = 'django-insecure-k*@d@0b3&e(l+r0v-2j)f(x!9_y_2_w+c1&z6c&l-g-p'

# Desative o modo de depuração em produção
DEBUG = True

ALLOWED_HOSTS = []

# Aplicações instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'signatures.apps.SignaturesConfig', # Sua aplicação de assinatura
    'corsheaders', # Novo: Adicionado para gerenciar as requisições CORS
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware', # Novo: Adicionado para gerenciar as requisições CORS
]

ROOT_URLCONF = 'mysite.urls'

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

WSGI_APPLICATION = 'mysite.wsgi.application'

# Configurações do Banco de Dados para SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Validação de Senhas
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

# Internacionalização
LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

# Tipo de campo de chave primária padrão
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Adicionado para permitir requisições de outras origens
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
]
CORS_ALLOW_ALL_ORIGINS = True # Permite todas as origens para simplificar a demo.
