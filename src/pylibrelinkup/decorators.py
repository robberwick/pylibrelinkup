from functools import wraps

from .exceptions import AuthenticationError


def authenticated(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.token is None:
            raise AuthenticationError("PyLibreLinkUp not authenticated")
        return func(self, *args, **kwargs)

    return wrapper
