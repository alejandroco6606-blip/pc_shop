"""
Django settings for pc_shop project.
...
"""

from pathlib import Path
import os
from dotenv import load_dotenv # <--- Ya tenías esto

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- NUEVO: Cargar variables de entorno ---
# Esto lee tu archivo .env (que creamos antes)
load_dotenv(os.path.join(BASE_DIR, '.env'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# --- CAMBIO: Secreto asegurado ---
# Lee la SECRET_KEY desde tu archivo .env
SECRET_KEY = os.getenv('SECRET_KEY') # <--- CAMBIO

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app_shop',     # Tu app "core" o de inventario (según tu estructura)
    'inventario',   # Tu app de inventario (si la separaste)
    'ventas',   # Tu app de ventas (¡Cuidado! creo la llamamos app_ventas, no 'ventas'. Ajústalo si es necesario)
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pc_shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # --- CAMBIO: Mejor práctica ---
        # Le decimos a Django que busque plantillas (como base.html) 
        # en una carpeta 'templates' en la raíz del proyecto.
        'DIRS': [BASE_DIR / 'templates'], # <--- CAMBIO
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

WSGI_APPLICATION = 'pc_shop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# --- CAMBIO: Base de datos asegurada ---
# Lee los datos de conexión desde tu archivo .env
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),         # <--- CAMBIO
        'USER': os.getenv('DB_USER'),         # <--- CAMBIO
        'PASSWORD': os.getenv('DB_PASSWORD'), # <--- CAMBIO
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# Password validation
# ... (sin cambios) ...
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


# Internationalization
# ... (sin cambios) ...
LANGUAGE_CODE = 'es-cl' # <--- CAMBIO (Recomendado para Chile)
TIME_ZONE = 'America/Santiago' # <--- CAMBIO (Recomendado para Chile)
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# --- NUEVO: Mejor práctica ---
# Le decimos a Django dónde buscar archivos estáticos (CSS/JS)
# en la raíz del proyecto.
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Default primary key field type
# ... (sin cambios) ...
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- CAMBIO: URLs de Login/Logout (corregidas) ---

LOGIN_URL = 'login' # Nombre de la ruta de tu vista de login

# A dónde ir después de un login exitoso.
# ¡Esto es clave! 'inventario:lista_productos' usa el "namespace" de tu app
# Si tu app de productos se llama 'inventario' en urls.py, esto es correcto.
LOGIN_REDIRECT_URL = 'lista_productos' # <--- AJUSTA ESTO a como lo tengas en tus URLs (ej: 'inventario:lista_productos')

# A dónde ir después de cerrar sesión
LOGOUT_REDIRECT_URL = 'login' # <--- CAMBIO (solo necesitas una)