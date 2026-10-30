from .api_url import APIUrl


class PyLibreLinkUpError(Exception):
    """Base class for PyLibreLinkUp exceptions."""

    pass


class AuthenticationError(PyLibreLinkUpError):
    """Raised when authentication fails."""

    pass


class RedirectError(PyLibreLinkUpError):
    """Raised when a redirect is encountered during authentication. This is a signal to retry the request with the new region.
    The region code is stored in the `region_code` attribute, and the API host to retry with in the `api_url` attribute.
    For backwards compatibility, the `region` attribute holds the matching APIUrl enum value, or None if the region has no
    APIUrl member.

    Prefer `api_url`: `region` reflects the static APIUrl enum, so it may be stale or None.
    """

    def __init__(self, region_code: str, api_url: str):
        self.region_code = region_code
        self.api_url = api_url
        try:
            self.region: APIUrl | None = APIUrl.from_string(region_code)
        except ValueError:
            self.region = None
        super().__init__(f"Redirected to {api_url}")


class UnknownRegionError(PyLibreLinkUpError):
    """Raised when a login redirect names a region with no known API host.
    The region code is stored in the `region` attribute of the exception.
    """

    def __init__(self, region: str):
        self.region = region
        super().__init__(f"Unknown region '{region}'")


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
