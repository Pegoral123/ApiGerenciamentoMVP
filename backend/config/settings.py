import os
from datetime import timedelta

import dj_database_url
from decouple import config

# Base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Segurança
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['*']

# URLs
ROOT_URLCONF = 'config.urls'

# Auth
AUTH_USER_MODEL = 'authentication.CustomUser'

# Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'drf_spectacular',
    'corsheaders',
    'apps.authentication',
    'apps.grupos',
    'apps.alunos',
    'apps.projetos',
    'apps.entregas',
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',   # ← adiciona o cors
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# Banco de dados
DATABASE_URL = config('DATABASE_URL', default=None)

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': config('DB_NAME', default='datagerenciamentomvp'),
            'USER': config('DB_USER', default='root'),
            'PASSWORD': config('DB_PASSWORD', default=''),
            'HOST': config('DB_HOST', default='127.0.0.1'),
            'PORT': config('DB_PORT', default='3306'),
        }
    }

SPECTACULAR_SETTINGS = {
    "TITLE": "Gerenciamento MVP API",
    "DESCRIPTION": "API do sistema de gerenciamento de projetos ADS",
    "VERSION": "1.0.0",
    "COMPONENT_SPLIT_REQUEST": True,
    "SERVE_INCLUDE_SCHEMA": False,
    "TAGS": [
        {
            "name": "Autenticação",
            "description": (
                "Endpoints responsáveis pelo controle de acesso ao sistema. "
                "Inclui login, geração e renovação de tokens JWT, logout com "
                "invalidação de sessão, cadastro de novos usuários, alteração "
                "de senha e consulta do perfil do usuário logado."
            ),
        },
        {
            "name": "Alunos",
            "description": (
                "Endpoints para gerenciamento completo dos alunos. "
                "Permite cadastrar, listar, buscar, editar, excluir e "
                "vincular alunos a grupos de projeto."
            ),
        },
        {
            "name": "Grupos",
            "description": (
                "Endpoints para gerenciamento das equipes de projeto. "
                "Permite criar, listar, editar e excluir grupos, além de "
                "consultar os alunos vinculados a cada equipe."
            ),
        },
        {
            "name": "Projetos",
            "description": (
                "Endpoints para gerenciamento dos projetos MVP. "
                "Permite criar, listar, editar e excluir projetos, "
                "com controle de status entre em andamento e concluído."
            ),
        },
        {
            "name": "Entregas",
            "description": (
                "Endpoints para gerenciamento das entregas e apresentações. "
                "Permite registrar entregas, marcar como apresentadas e "
                "adicionar links de apresentação por projeto."
            ),
        },
    ],
    "APPEND_COMPONENTS": {
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }
    },
    "SECURITY": [{"bearerAuth": []}],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME':    timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME':   timedelta(days=7),
    'ROTATE_REFRESH_TOKENS':    True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES':        ('Bearer',),
}

# CORS — permite o frontend acessar a API
CORS_ALLOW_ALL_ORIGINS = True   # ← em produção trocar pelo domínio do front

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'