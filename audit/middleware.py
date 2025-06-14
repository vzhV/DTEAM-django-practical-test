from .models import RequestLog
from .constants import SKIP_LOG_PATHS


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not any(request.path.startswith(p) for p in SKIP_LOG_PATHS):
            remote_ip = (
                request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip()
                or request.META.get('REMOTE_ADDR')
                or None
            )
            RequestLog.objects.create(
                method=request.method[:8],
                path=request.path[:512],
                query_string=request.META.get('QUERY_STRING', ''),
                remote_ip=remote_ip,
            )
        return self.get_response(request)
