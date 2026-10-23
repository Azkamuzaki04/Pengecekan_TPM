from pathlib import Path

# =========================================================
# BASE DIRECTORY
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================================================
# SECURITY
# =========================================================

SECRET_KEY = "dev-only-change-this-in-production"

DEBUG = True


# =========================================================
# ALLOWED HOSTS
# =========================================================

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "10.162.65.131",
]


# =========================================================
# CSRF TRUSTED ORIGINS
# =========================================================
# Penting untuk menghindari error:
# "Forbidden (403)"
# "CSRF verification failed"
#
# Karena aplikasi bisa dibuka melalui:
# localhost
# 127.0.0.1
# 10.28.158.131
# =========================================================

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://10.28.158.131:8000",
]


# =========================================================
# APPLICATIONS
# =========================================================

INSTALLED_APPS = [

    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Project Apps
    "accounts",
    "barang",
    "inspection",
    "reports",
    "server",

    # REST API
    "rest_framework",
    "rest_framework.authtoken",
    "api",
]


# =========================================================
# MIDDLEWARE
# =========================================================

MIDDLEWARE = [

    "django.middleware.security.SecurityMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    # CSRF
    "django.middleware.csrf.CsrfViewMiddleware",

    # Authentication
    "django.contrib.auth.middleware.AuthenticationMiddleware",

    # Messages
    "django.contrib.messages.middleware.MessageMiddleware",

    # Security
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# =========================================================
# URL CONFIGURATION
# =========================================================

ROOT_URLCONF = "config.urls"


# =========================================================
# TEMPLATES
# =========================================================

TEMPLATES = [

    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates"
        ],

        "APP_DIRS": True,

        "OPTIONS": {

            "context_processors": [

                "django.template.context_processors.request",

                "django.contrib.auth.context_processors.auth",

                "django.contrib.messages.context_processors.messages",

            ],
        },
    },
]


# =========================================================
# WSGI
# =========================================================

WSGI_APPLICATION = "config.wsgi.application"


# =========================================================
# DATABASE
# =========================================================
# MySQL XAMPP / phpMyAdmin
#
# DATABASE:
# checksheet
#
# USER:
# root
#
# PASSWORD:
# kosong
#
# PORT:
# 3306
#
# Jangan hapus database lama.
# =========================================================

DATABASES = {

    "default": {

        "ENGINE": "django.db.backends.mysql",

        "NAME": "checksheet",

        "USER": "root",

        "PASSWORD": "",

        "HOST": "127.0.0.1",

        "PORT": "3306",

    }
}


# =========================================================
# PASSWORD VALIDATION
# =========================================================

AUTH_PASSWORD_VALIDATORS = [

    {
        "NAME":
        "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },

    {
        "NAME":
        "django.contrib.auth.password_validation.MinimumLengthValidator",
    },

    {
        "NAME":
        "django.contrib.auth.password_validation.CommonPasswordValidator",
    },

    {
        "NAME":
        "django.contrib.auth.password_validation.NumericPasswordValidator",
    },

]


# =========================================================
# LANGUAGE
# =========================================================

LANGUAGE_CODE = "id"


# =========================================================
# TIME ZONE
# =========================================================

TIME_ZONE = "Asia/Jakarta"


# =========================================================
# INTERNATIONALIZATION
# =========================================================

USE_I18N = True

USE_TZ = True


# =========================================================
# STATIC FILES
# =========================================================

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static"
]


# =========================================================
# MEDIA / UPLOAD FILES
# =========================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# =========================================================
# DEFAULT PRIMARY KEY
# =========================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =========================================================
# LOGIN / LOGOUT
# =========================================================

LOGIN_URL = "/login/"

LOGIN_REDIRECT_URL = "/dashboard/"

LOGOUT_REDIRECT_URL = "/login/"


# =========================================================
# DJANGO REST FRAMEWORK
# =========================================================

REST_FRAMEWORK = {

    "DEFAULT_AUTHENTICATION_CLASSES": [

        "rest_framework.authentication.TokenAuthentication",

    ],

}


# =========================================================
# SESSION
# =========================================================
# Membantu session login tetap stabil selama browser
# masih digunakan.
# =========================================================

SESSION_COOKIE_AGE = 60 * 60 * 8  # 8 jam

SESSION_SAVE_EVERY_REQUEST = True

SESSION_COOKIE_HTTPONLY = True

SESSION_COOKIE_SAMESITE = "Lax"


# =========================================================
# CSRF COOKIE
# =========================================================

CSRF_COOKIE_HTTPONLY = False

CSRF_COOKIE_SAMESITE = "Lax"

CSRF_USE_SESSIONS = False


# =========================================================
# SECURITY DEVELOPMENT SETTINGS
# =========================================================
# Jangan aktifkan SECURE_SSL_REDIRECT karena aplikasi
# masih menggunakan HTTP lokal.
# =========================================================