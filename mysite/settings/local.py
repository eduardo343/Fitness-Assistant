import os

from .base import *  # noqa: F403
from .base import _env_bool, _env_list

DEBUG = _env_bool("DJANGO_DEBUG", default=True)
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-local-dev-key")
ALLOWED_HOSTS = _env_list("DJANGO_ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])
CSRF_TRUSTED_ORIGINS = _env_list("DJANGO_CSRF_TRUSTED_ORIGINS", default=[])
ENABLE_ADMIN = _env_bool("ENABLE_ADMIN", default=True)
