from __future__ import annotations

from uuid import UUID

import requests
from pydantic import ValidationError

from .api_url import APIUrl
from .decorators import authenticated
from .exceptions import (
    AuthenticationError,
    RedirectError,
    TermsOfUseError,
    PrivacyPolicyError,
    EmailVerificationError,
)
from .models.connection import GraphResponse, LogbookResponse
from .models.data import Patient
from .models.login import LoginArgs
from .utilities import coerce_patient_id

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
            case "verifyEmail":
                raise EmailVerificationError()

        try:
            self.token = data["data"]["authTicket"]["token"]
            self.HEADERS.update({"authorization": "Bearer " + self.token})

        except KeyError:
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

    def _get_logbook_json(self, patient_id: UUID) -> dict:
        r = requests.get(
            url=f"{self.api_url}/llu/connections/{patient_id}/logbook",
            headers=self.HEADERS,
        )
        r.raise_for_status()
        return r.json()

    @authenticated
    def read(self, patient_identifier: UUID | str | Patient) -> GraphResponse:
        """Requests and returns patient data"""
        patient_id = coerce_patient_id(patient_identifier)

        response_json = self._get_graph_data_json(patient_id)

        return GraphResponse.model_validate(response_json)

    @authenticated
    def logbook(self, patient_identifier: UUID | str | Patient) -> LogbookResponse:
        """Requests and returns patient logbook data"""
        patient_id = coerce_patient_id(patient_identifier)

        response_json = self._get_logbook_json(patient_id)

        return LogbookResponse.model_validate(response_json)
