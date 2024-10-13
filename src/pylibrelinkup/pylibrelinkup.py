from __future__ import annotations

import hashlib
from uuid import UUID

import requests
from pydantic import ValidationError

from .api_url import APIUrl
from .exceptions import (
    AuthenticationError,
    RedirectError,
    TermsOfUseError,
    PrivacyPolicyError,
)
from .models.connection import ConnectionResponse
from .models.data import Patient
from .models.login import LoginArgs, LoginResponse

__all__ = ["PyLibreLinkUp"]


HEADERS: dict[str, str] = {
    "accept-encoding": "gzip",
    "cache-control": "no-cache",
    "connection": "Keep-Alive",
    "content-type": "application/json",
    "product": "llu.android",
    "version": "4.11.0",
}


class PyLibreLinkUp:
    """PyLibreLinkUp class to request data from the LibreLinkUp API."""

    email: str
    password: str
    token: str | None
    account_id_hash: str | None

    def __init__(self, email: str, password: str, api_url: APIUrl = APIUrl.US):
        self.login_args: LoginArgs = LoginArgs(email=email, password=password)
        self.email = email or ""
        self.password = password or ""
        self.token = None
        self.account_id_hash = None
        self.api_url: str = api_url.value

    def authenticate(self) -> None:
        r = requests.post(
            url=f"{self.api_url}/llu/auth/login",
            headers=self._get_headers(),
            json=self.login_args.model_dump(),
        )
        r.raise_for_status()
        data = r.json()
        # Response to login can either be a request to use a different regional host, just successful, or a request
        # to accept terms or privacy policy.
        data_dict = data.get("data", {})
        if data_dict.get("redirect", False):
            raise RedirectError(APIUrl.from_string(data_dict["region"].upper()))

        match data_dict.get("step", {}).get("type"):
            case "tou":
                raise TermsOfUseError()
            case "pp":
                raise PrivacyPolicyError()

        try:
            login_response = LoginResponse.model_validate(data)
            self._set_token(login_response.data.authTicket.token)
            self._set_account_id_hash(login_response.data.user.id)

        except ValidationError:
            raise AuthenticationError("Invalid login credentials")

    def _set_token(self, token: str):
        """Saves the token for future requests."""
        self.token = token

    def _get_headers(self) -> dict:
        """Returns the headers for the request."""
        headers = HEADERS.copy()
        if self.token:
            headers.update({"authorization": "Bearer " + self.token})
        if self.account_id_hash:
            headers.update({"account-id": self.account_id_hash})
        return headers

    def get_patients(self) -> list[Patient]:
        """Requests and returns patient data"""
        r = requests.get(
            url=f"{self.api_url}/llu/connections", headers=self._get_headers()
        )
        r.raise_for_status()
        data = r.json()
        return [Patient.model_validate(patient) for patient in data["data"]]

    def _get_graph_data_json(self, patient_id: UUID) -> dict:
        r = requests.get(
            url=f"{self.api_url}/llu/connections/{patient_id}/graph",
            headers=self._get_headers(),
        )
        r.raise_for_status()
        return r.json()

    def read(self, patient_identifier: UUID | str | Patient) -> ConnectionResponse:
        """Requests and returns patient data"""
        if self.token is None:
            raise AuthenticationError("PyLibreLinkUp not authenticated")

        invalid_patient_identifier = "Invalid patient_identifier"
        patient_id: UUID | None = None
        if isinstance(patient_identifier, UUID):
            patient_id = patient_identifier
        elif isinstance(patient_identifier, str):
            try:
                patient_id = UUID(patient_identifier)
            except ValueError as exc:
                raise ValueError(invalid_patient_identifier) from exc
        elif isinstance(patient_identifier, Patient):
            patient_id = patient_identifier.patient_id
        else:
            raise ValueError(invalid_patient_identifier)

        response_json = self._get_graph_data_json(patient_id)

        return ConnectionResponse.model_validate(response_json)

    def _set_account_id_hash(self, account_id: str):
        """Saves the account_id_hash for future requests."""
        self.account_id_hash = hashlib.sha256(account_id.encode()).hexdigest()
