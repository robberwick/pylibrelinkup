from .exceptions import AuthenticationError


def authenticated(func):
    def wrapper(self, *args, **kwargs):
        if self.token is None:
            raise AuthenticationError("PyLibreLinkUp not authenticated")
        return func(self, *args, **kwargs)

    return wrapper
