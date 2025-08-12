
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

print("DEBUG raw value:", os.getenv("DEBUG"))


#DEBUG =  os.getenv("DEBUG")
BASE_DIR = Path(__file__).resolve().parent.parent
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")  # "prod" or "dev"
#DB_ENGINE = os.getenv("DB_ENGINE").lower()
STATIC_ROOT = BASE_DIR / 'staticfiles'
SECRET_KEY = 'django-insecure-g&=)-s8my*@7q83-wxe4nx3i(jjm9-#-85h%n9gf-a9(-tiplg'
ALLOWED_HOSTS = ["*"]


LOGIN_URL="django_auth_adfs:login"  
LOGIN_REDIRECT_URL = '/hub/'
LOGOUT_REDIRECT_URL = "/logged-out/"  # or whatever landing page



OIDC_AUTHENTICATION_CALLBACK_URL = 'oidc_authentication_callback'
OIDC_RP_CLIENT_ID = os.getenv('OIDC_CLIENT_ID')
OIDC_RP_CLIENT_SECRET = os.getenv('OIDC_CLIENT_SECRET')
OIDC_TENANT_ID = os.getenv('OIDC_TENANT_ID')
OIDC_OP_AUTHORIZATION_ENDPOINT = f'https://login.microsoftonline.com/{OIDC_TENANT_ID}/oauth2/v2.0/authorize'
OIDC_OP_TOKEN_ENDPOINT = f'https://login.microsoftonline.com/{OIDC_TENANT_ID}/oauth2/v2.0/token'
OIDC_OP_USER_ENDPOINT = 'https://graph.microsoft.com/oidc/userinfo'
OIDC_OP_JWKS_ENDPOINT = f'https://login.microsoftonline.com/{OIDC_TENANT_ID}/discovery/v2.0/keys'
OIDC_OP_LOGOUT_ENDPOINT = f'https://login.microsoftonline.com/{OIDC_TENANT_ID}/oauth2/v2.0/logout'
OIDC_RP_SIGN_ALGO = 'RS256'
OIDC_RP_SAVE_SESSION = True
OIDC_STORE_ID_TOKEN = True
OIDC_STORE_ACCESS_TOKEN = True
OIDC_LOGOUT_REDIRECT_URL = '/logged-out/'



# Email settings
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'false').lower() == 'true'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)
DJANGO_SETTINGS_MODULE = os.getenv('DJANGO_SETTINGS_MODULE')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_auth_adfs',
    'core',
    'contacts',
    'invoices',
    'crispy_forms',
    'crispy_bootstrap5',
    'widget_tweaks',
    'ccbot',  # Add your new app here
]

CRISPY_ALLOWED_TEMPLATE_PACKS = ["bootstrap5"]
CRISPY_TEMPLATE_PACK = "bootstrap5"

TIME_ZONE = 'America/Los_Angeles'
USE_TZ = True
AUTHENTICATION_BACKENDS = [
    'django_auth_adfs.backend.AdfsAuthCodeBackend',
    'django.contrib.auth.backends.ModelBackend', # path to your custom backend
    #'core.oidc.AzureOIDCBackend',  # NOT USED ANYMORE during migration

 ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django_auth_adfs.middleware.LoginRequiredMiddleware",
]

ROOT_URLCONF = 'base_app.urls'

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

WSGI_APPLICATION = 'base_app.wsgi.application'



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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




# =======================
# Database config
# =======================
if os.getenv("POSTGRES_DB"):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_DB'),
            'USER': os.getenv('POSTGRES_USER'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
            'HOST': os.getenv('POSTGRES_HOST', '127.0.0.1'),
            'PORT': os.getenv('POSTGRES_PORT', '5432'),
        }
    }
    print(f"📦 Using **Postgres** DB: {DATABASES['default']['NAME']} at {DATABASES['default']['HOST']}:{DATABASES['default']['PORT']}")
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    print(f"📦 Using **SQLite** DB at {DATABASES['default']['NAME']}")




# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'



# Trust X-Forwarded headers from Azure App Proxy or NGINX
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
X_FRAME_OPTIONS = 'SAMEORIGIN'


#ADDED
CSRF_TRUSTED_ORIGINS = [
    "https://app.stopwaste.org",
    "https://stopwastedjangoapp-stopwaste.msappproxy.net",
]

AUTH_ADFS = {
    "AUDIENCE": "6150bd55-28c1-4616-9da7-f68b411ebbae",
    "CLIENT_ID": os.getenv("OIDC_CLIENT_ID"),
    "CLIENT_SECRET": os.getenv("OIDC_CLIENT_SECRET"),  # make sure you have this set in your environment
    "CLAIM_MAPPING": {
        "first_name": "given_name",
        "last_name": "family_name",
        "email": "upn",          # or "email" depending on your tenant's claims
    },
    "USERNAME_CLAIM": "upn",    # how Django will identify the user
    "RELYING_PARTY_ID": os.getenv("OIDC_CLIENT_ID"),
    "VERSION": "v1.0",          # probably "v2.0" for Azure AD
    "TENANT_ID": os.getenv("OIDC_TENANT_ID"),  # ✅ Add this line
    "LOGIN_EXEMPT_URLS": [
        r"^health/",
        r"^static/",            # skip static files
    ],
    # Make sure this is your Azure Application Proxy URL + callback path:
}








