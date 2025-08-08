from base_app.settings import *  # Import everything from main settings.py

print("✅ LOADED: base_app.settings_dev")

DEBUG = True

SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-dev-secret')

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}

# Optionally override static/media if needed (they're fine if inherited)
# STATICFILES_DIRS = [BASE_DIR / 'core' / 'static']
# MEDIA_ROOT = BASE_DIR / 'media'
