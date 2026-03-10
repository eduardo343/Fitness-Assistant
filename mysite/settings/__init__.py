import os


def _resolve_settings_env():
    configured_env = os.getenv("DJANGO_ENV")
    if configured_env:
        return configured_env.strip().lower()
    if os.getenv("VERCEL") or os.getenv("VERCEL_ENV"):
        return "production"
    return "local"


SETTINGS_ENV = _resolve_settings_env()

if SETTINGS_ENV == "production":
    from .production import *  # noqa: F403
elif SETTINGS_ENV == "local":
    from .local import *  # noqa: F403
else:
    raise RuntimeError(f"Unsupported DJANGO_ENV value: {SETTINGS_ENV}")
