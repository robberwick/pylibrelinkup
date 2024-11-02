from __future__ import annotations

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


class PyLibreLinkUp:
    """PyLibreLinkUp class to request data from the LibreLinkUp API."""

    email: str
    password: str
    token: str | None

    HEADERS = {
        "accept-encoding": "gzip",
        "cache-control": "no-cache",
        "connection": "Keep-Alive",
        "content-type": "application/json",
        "product": "llu.android",
        "version": "4.7.0",
    }

    def __init__(self, email: str, password: str, api_url: APIUrl = APIUrl.US):
        self.login_args: LoginArgs = LoginArgs(email=email, password=password)
        self.email = email or ""
        self.password = password or ""
        self.token = None
        self.api_url: str = api_url.value

    def authenticate(self) -> None:
        r = requests.post(
            url=f"{self.api_url}/llu/auth/login",
            headers=self.HEADERS,
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
            self.token = login_response.data.authTicket.token
            self.HEADERS.update({"authorization": "Bearer " + self.token})

        except ValidationError:
            raise AuthenticationError("Invalid login credentials")

    def get_patients(self) -> list[Patient]:
        """Requests and returns patient data"""
        r = requests.get(url=f"{self.api_url}/llu/connections", headers=self.HEADERS)
        r.raise_for_status()
        data = r.json()
        return [Patient.model_validate(patient) for patient in data["data"]]

    def _get_graph_data_json(self, patient_id: UUID) -> dict:
        r = requests.get(
            url=f"{self.api_url}/llu/connections/{patient_id}/graph",
            headers=self.HEADERS,
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
