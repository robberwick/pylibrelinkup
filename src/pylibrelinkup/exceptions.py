from .api_url import APIUrl

__all__ = ["AuthenticationError", "RedirectError", "TermsOfUseError"]


class AuthenticationError(Exception):
    """Raised when authentication fails."""

    pass


class RedirectError(Exception):
    """Raised when a redirect is encountered during authentication. This is a signal to retry the request with the new region.
    The new region is stored in the `region` attribute of the exception, which is an APIUrl enum value.
    """

    def __init__(self, region: APIUrl):
        self.region = region
        super().__init__(f"Redirected to {region}")


class TermsOfUseError(Exception):
    """Raised when the user needs to accept terms of use."""

    def __init__(self):
        super().__init__("User needs to accept terms of use. ")


class PrivacyPolicyError(Exception):
    """Raised when the user needs to accept the privacy policy."""

    def __init__(self):
        super().__init__("User needs to accept the privacy policy. ")
