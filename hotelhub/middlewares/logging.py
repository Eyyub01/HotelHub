import logging

logger = logging.getLogger("django")


class RequestLoggingMiddleware:
    """Middleware to log request details including user and IP address."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        ip = self.get_client_ip(request)

        logger.info(f"[{request.method}] {request.path} - Requested by {user} from {ip}")

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Get client IP address from request."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip