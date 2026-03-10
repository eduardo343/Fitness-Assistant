import os

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403
from .base import _env_bool, _env_list

DEBUG = _env_bool("DJANGO_DEBUG", default=False)

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY") or os.getenv("SECRET_KEY", "")
if not SECRET_KEY:
    raise ImproperlyConfigured(
        "Set DJANGO_SECRET_KEY or SECRET_KEY for production deployments."
    )

default_allowed_hosts = ["127.0.0.1", "localhost", ".vercel.app"]
vercel_url = os.getenv("VERCEL_URL")
if vercel_url:
    default_allowed_hosts.append(vercel_url)

ALLOWED_HOSTS = _env_list("DJANGO_ALLOWED_HOSTS", default=default_allowed_hosts)

default_csrf_trusted_origins = ["https://*.vercel.app"] if ON_VERCEL else []  # noqa: F405
if vercel_url:
    default_csrf_trusted_origins.append(f"https://{vercel_url}")

CSRF_TRUSTED_ORIGINS = _env_list(
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    default=default_csrf_trusted_origins,
)

ENABLE_ADMIN = _env_bool("ENABLE_ADMIN", default=False)

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
