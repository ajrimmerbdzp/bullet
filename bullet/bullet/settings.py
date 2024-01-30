import os
import random
import socket
from pathlib import Path

import environ
from django_countries.widgets import LazyChoicesMixin

import bullet

# monkey-patched django-countries
LazyChoicesMixin.get_choices = lambda self: self._choices
LazyChoicesMixin.choices = property(
    LazyChoicesMixin.get_choices, LazyChoicesMixin.set_choices
)

env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent

# This will be overwritten by prod ENV
SECRET_KEY = env(
    "SECRET_KEY",
    default="django-insecure-3qj^lv&gv&rq&6ef5f1xuvu(s-7++e)b0x0#&qq0uy&dx^!d7^",
)
DEBUG = env("DEBUG", default=False)

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 3600

ALLOWED_HOSTS = env(
    "DJANGO_ALLOWED_HOSTS",
    default=[
        "localhost",
        "math.localhost",
        "physics.localhost",
        "junior.localhost",
        "chemistry.localhost",
        "admin.localhost",
    ],
)

INSTALLED_APPS = [
    "address",
    "phonenumber_field",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "widget_tweaks",
    #
    "users",
    "competitions",
    "web",
    "bullet_admin",
    "education",
    "countries",
    "problems",
    "documents",
    #
    "django_countries",
    "django_recaptcha",
    "django_minify_html",
    "fontawesomefree",
    "django_htmx",
    "silk",
    "simple_history",
    "django_web_components",
    "django_rq",
    "django_probes",
    "debug_toolbar",
    "pictures",
    "gallery",
]

DATABASES = {
    "default": env.db(default="postgres://bullet:bullet@db/bullet"),
}

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "web.middleware.AdminDomainMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "silk.middleware.SilkyMiddleware",
    "competitions.middleware.BranchMiddleware",
    "countries.middleware.CountryLanguageMiddleware",
    "web.middleware.BulletMinifyHtmlMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

PARENT_HOST = env("PARENT_HOST", default="naboj.org")
ROOT_URLCONF = "web.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "web.context_processors.menu_context",
                "web.context_processors.branch_context",
                "web.context_processors.version_context",
                "django.template.context_processors.i18n",
            ],
            "builtins": [
                "django_web_components.templatetags.components",
            ],
        },
    },
]

WSGI_APPLICATION = "bullet.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = "users.User"
LOGIN_URL = "badmin:login"
LOGIN_REDIRECT_URL = "badmin:home"
SESSION_COOKIE_NAME = "bullet_session"
CSRF_COOKIE_NAME = "bullet_csrf_token"

LANGUAGE_CODE = "en"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)

DEFAULT_FROM_EMAIL = env("EMAIL_FROM", default="devel@naboj.org")
EMAIL_CONFIG = env.email("EMAIL_URL", default="consolemail://")
vars().update(EMAIL_CONFIG)

# These are Google's testing keys
RECAPTCHA_PUBLIC_KEY = env(
    "RECAPTCHA_PUBLIC_KEY", default="6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
)
RECAPTCHA_PRIVATE_KEY = env(
    "RECAPTCHA_PRIVATE_KEY", default="6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"
)
MEDIA_ROOT = BASE_DIR / "uploads"
MEDIA_URL = "/uploads/"
GEOIP_PATH = "/geoip/"

MEILISEARCH_URL = env("MEILISEARCH_URL", default="http://meilisearch:7700/")
MEILISEARCH_KEY = env("MEILISEARCH_KEY", default=None)

PROBLEM_SOLVE_KEY = env("PROBLEM_SOLVE_KEY", default="")


def silky_intercept(request):
    if request.path.startswith("/silk/"):
        return False
    return random.random() < 0.1


SILKY_AUTHENTICATION = True
SILKY_AUTHORISATION = True
SILKY_INTERCEPT_FUNC = silky_intercept
SILKY_MAX_RECORDED_REQUESTS_CHECK_PERCENT = 0

RQ_QUEUES = {
    "default": {
        "HOST": env("REDIS_HOST", default="redis"),
        "PORT": env("REDIS_PORT", default=6379),
        "DB": env("REDIS_DB", default=0),
        "ASYNC": env("REDIS_RQ_ASYNC", default=True),
    },
}

dsn = env("SENTRY_DSN", default="")
if dsn:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=dsn,
        integrations=[DjangoIntegration()],
        auto_session_tracking=False,
        traces_sample_rate=0,
        send_default_pii=True,
        release=bullet.VERSION,
    )

if DEBUG:
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ips + ["127.0.0.1"]
    SILENCED_SYSTEM_CHECKS = ["django_recaptcha.recaptcha_test_key_error"]
else:
    SESSION_COOKIE_DOMAIN = env("PARENT_HOST", default="naboj.org")
    SESSION_COOKIE_SECURE = True

PICTURES = {
    "BREAKPOINTS": {
        "xs": 576,
        "s": 768,
        "m": 992,
        "l": 1200,
        "xl": 1400,
    },
    "GRID_COLUMNS": 4,
    "CONTAINER_WIDTH": 1200,
    "FILE_TYPES": ["WEBP"],
    "PIXEL_DENSITIES": [1, 2],
    "USE_PLACEHOLDERS": False,
    "QUEUE_NAME": "pictures",
    "PROCESSOR": "pictures.tasks.process_picture",
}
