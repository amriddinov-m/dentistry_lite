# company/middleware.py
import threading

_request_local = threading.local()


class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Сохраняем текущий объект запроса в локальном хранилище
        _request_local.request = request
        print(f"RequestMiddleware: {request}")
        response = self.get_response(request)
        return response


def get_current_request():
    # Возвращаем текущий объект запроса из локального хранилища
    return getattr(_request_local, 'request', None)
