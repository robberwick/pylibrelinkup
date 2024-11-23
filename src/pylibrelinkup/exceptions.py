from .api_url import APIUrl


class PyLibreLinkUpError(Exception):
    """Base class for PyLibreLinkUp exceptions."""

    pass


class AuthenticationError(PyLibreLinkUpError):
    """Raised when authentication fails."""

    pass


class RedirectError(PyLibreLinkUpError):
    """Raised when a redirect is encountered during authentication. This is a signal to retry the request with the new region.
    The new region is stored in the `region` attribute of the exception, which is an APIUrl enum value.
    """

    def __init__(self, region: APIUrl):
        self.region = region
        super().__init__(f"Redirected to {region}")


class TermsOfUseError(PyLibreLinkUpError):
    """Raised when the user needs to accept terms of use."""

    def __init__(self):
        super().__init__("User needs to accept terms of use. ")


class PrivacyPolicyError(PyLibreLinkUpError):
    """Raised when the user needs to accept the privacy policy."""

    def __init__(self):
        super().__init__("User needs to accept the privacy policy. ")


class EmailVerificationError(PyLibreLinkUpError):
    """Raised when the user needs to verify their email."""

    def __init__(self):
        super().__init__("User needs to verify their email. ")
