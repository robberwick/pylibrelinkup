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


class PatientNotFoundError(PyLibreLinkUpError):
    """Raised when a patient with the provided patient_id is not found."""

    def __init__(self):
        super().__init__("Patient not found")


class LLUAPIError(PyLibreLinkUpError):
    """Raised when the LibreLinkUp API returns an error."""

    def __init__(self, response_code: int, message: str):
        self.response_code = response_code
        exception_message = f"LLU API returned error {response_code}: {message}"
        super().__init__(exception_message)


class LLUAPIRateLimitError(LLUAPIError):
    """Raised when the LibreLinkUp API returns a rate limit error."""

    retry_after: int | None

    def __init__(
        self, response_code: int, message: str, retry_after: int | None = None
    ):
        self.retry_after = retry_after
        super().__init__(response_code, message)
