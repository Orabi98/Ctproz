# buildright/settings.py
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# --- .env (optional for local dev) ---
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env", override=True)
except Exception:
    pass

# --- Core ---
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-insecure-key-change-me")
DEBUG = os.getenv("DJANGO_DEBUG", "True").lower() in ("1", "true", "yes")

# Comma-separated hostnames, e.g. "localhost,127.0.0.1,app.onrender.com"
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# Comma-separated CSRF trusted origins, e.g. "https://app.onrender.com,https://*.yourdomain.com"
_csrf_origins = os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "")
CSRF_TRUSTED_ORIGINS = [o.strip() for o in _csrf_origins.split(",") if o.strip()]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "website",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise must be right after SecurityMiddleware
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "buildright.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "buildright.wsgi.application"
ASGI_APPLICATION = "buildright.asgi.application"

# --- Database ---
# Default: sqlite for local dev
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# If DATABASE_URL is provided (Render/Heroku), use it.
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    try:
        import dj_database_url

        DATABASES["default"] = dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=os.getenv("DATABASE_SSL_REQUIRE", "False").lower() in ("1", "true", "yes"),
        )
    except Exception:
        # If dj_database_url isn't available locally, keep sqlite.
        pass

# --- Password validation ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- i18n / tz ---
LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/New_York"
USE_I18N = True
USE_TZ = True

# --- Static / Media ---
# IMPORTANT: must start with a leading slash
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]   # your source assets in dev
STATIC_ROOT = BASE_DIR / "staticfiles"     # collectstatic output in prod

# WhiteNoise hashed/compressed storage
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# (Optional) If you add user uploads later:
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# --- Email (Gmail / Google Workspace via SMTP) ---
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() in ("1", "true", "yes")

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "info@ctproz.com")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")  # Use an App Password in prod
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# Admin error email recipients (for mail_admins, etc.)
ADMINS = [("CTProz Site", "info@ctproz.com")]

# --- Security (auto-relax when DEBUG=True) ---
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = os.getenv("DJANGO_SECURE_SSL_REDIRECT", "True").lower() in ("1", "true", "yes")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # Prevent browser from inferring MIME types
    SECURE_CONTENT_TYPE_NOSNIFF = True
    # Basic clickjacking protection already enabled via middleware; optionally:
    X_FRAME_OPTIONS = "DENY"

# --- Default PK ---
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Minimal logging helpful in prod ---
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {"handlers": ["console"], "level": "INFO"},
}
