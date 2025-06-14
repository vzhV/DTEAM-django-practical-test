from django.conf import settings


def settings_context(request):
    """
    Injects the Django settings into the template context as 'settings'.
    """
    return {
        'settings': settings,
        "APP_VERSION": getattr(settings, "APP_VERSION", "unknown"),
    }
