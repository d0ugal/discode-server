from limits import storage
from limits import strategies
from limits import parse
from sanic import exceptions


class TooManyRequests(exceptions.InvalidUsage):
    status_code = 429


_MEMORY_STORAGE = storage.MemoryStorage()
_MOVING_WINDOW = strategies.MovingWindowRateLimiter(_MEMORY_STORAGE)

_LIMIT_MESSAGE = "Paste creation limited at 6 per minute."


def limiter(frequency):
    frequency = parse(frequency)

    def decorator(function):
        def wrapper(request, *args, **kwargs):
            namespace = f"{function.__module__}.{function.__name__}"
            ip = request.ip[0] or '127.0.0.1'
            print(ip)
            ip = request.headers.get("X-Forwarded-For", ip)
            print(namespace, ip)
            print(_MOVING_WINDOW.get_window_stats(frequency, namespace, ip))
            if not _MOVING_WINDOW.hit(frequency, namespace, ip):
                raise TooManyRequests(_LIMIT_MESSAGE)
            return function(request, *args, **kwargs)
        return wrapper
    return decorator
