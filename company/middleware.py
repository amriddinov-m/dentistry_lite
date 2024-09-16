import threading

_request_local = threading.local()


class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _request_local.request = request
        _request_local.user = request.user
        return self.get_response(request)


def get_current_user():
    return getattr(_request_local, 'user', None)
