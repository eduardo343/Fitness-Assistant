from django.conf import settings


def app_meta(_request):
    return {
        "APP_STAGE": getattr(settings, "APP_STAGE", "demo").upper(),
        "DEMO_MODE": getattr(settings, "DEMO_MODE", True),
        "SETTINGS_ENV": getattr(settings, "SETTINGS_ENV", "local"),
    }
