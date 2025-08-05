
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()




DEBUG = os.getenv("DEBUG", "false").lower() == "true"
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")  # "prod" or "dev"



#APP_PROXY_CALLBACK = os.getenv("APP_PROXY_CALLBACK", "https://stopwastedjangoapp-stopwaste.msappproxy.net/oidc/callback/")
#probably dont need these next 2 - will experiment wiht decomisison 
#LOCAL_CALLBACK = os.getenv("LOCAL_CALLBACK", "http://localhost:8000/oidc/callback/")
#INTERNAL_HOST = os.getenv("INTERNAL_HOST", "http://localhost:8000")
#end dont need probably 

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


BASE_DIR = Path(__file__).resolve().parent.parent

print("✅ BASE_DIR =", BASE_DIR)


STATIC_ROOT = BASE_DIR / 'staticfiles'
SECRET_KEY = 'django-insecure-g&=)-s8my*@7q83-wxe4nx3i(jjm9-#-85h%n9gf-a9(-tiplg'

#ADDED 
#ALLOWED_HOSTS = ["0.0.0.0", "127.0.0.1","10.1.3.66", "localhost","app.stopwaste.org",  "stopwastedjangoapp-stopwaste.msappproxy.net",]
ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_auth_adfs',
    #'books',
    #'mozilla_django_oidc',
    'core',
    'invoices',
    'crispy_forms',
    'crispy_bootstrap5',
    'widget_tweaks',
    'ccbot',  # Add your new app here
]

CRISPY_ALLOWED_TEMPLATE_PACKS = ["bootstrap5"]
CRISPY_TEMPLATE_PACK = "bootstrap5"


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


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'stopwasteapps'),
        'USER': os.getenv('POSTGRES_USER', 'stopwaste'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'BlinkusGaladrigal'),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'





STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
#STATICFILES_DIRS = [
#    BASE_DIR / 'core' / 'static',
#]

#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

X_FRAME_OPTIONS = 'SAMEORIGIN'

# Trust X-Forwarded headers from Azure App Proxy or NGINX
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True



#ADDED
CSRF_TRUSTED_ORIGINS = [
    "https://app.stopwaste.org",
    "https://stopwastedjangoapp-stopwaste.msappproxy.net",
]


import os

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








