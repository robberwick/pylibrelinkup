from __future__ import annotations

import warnings
from typing import List
from uuid import UUID

import requests
from pydantic import ValidationError

from .api_url import APIUrl
from .decorators import authenticated
from .exceptions import (
    AuthenticationError,
    EmailVerificationError,
    PrivacyPolicyError,
    RedirectError,
    TermsOfUseError,
)
from .models.connection import GraphResponse, LogbookResponse
from .models.data import GlucoseMeasurement, Patient
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
        """Authenticate with the LibreLinkUp API"""
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

    def _call_api(self, url: str = None) -> dict:
        r = requests.get(url=url, headers=self.HEADERS)
        r.raise_for_status()
        data = r.json()
        return data

    def get_patients(self) -> list[Patient]:
        """Requests and returns patient data"""
        data = self._call_api(url=f"{self.api_url}/llu/connections")
        return [Patient.model_validate(patient) for patient in data["data"]]

    def _get_graph_data_json(self, patient_id: UUID) -> dict:
        """Requests and returns patient graph data"""
        return self._call_api(url=f"{self.api_url}/llu/connections/{patient_id}/graph")

    def _get_logbook_json(self, patient_id: UUID) -> dict:
        """Requests and returns patient logbook data"""
        return self._call_api(
            url=f"{self.api_url}/llu/connections/{patient_id}/logbook"
        )

    @authenticated
    def read(self, patient_identifier: UUID | str | Patient) -> GraphResponse:
        """Requests and returns patient data"""
        # raise a deprecation warning for this method in favor of the graph method
        warnings.warn(
            "The read method is deprecated. Instead, please use the graph method for retrieving graph data,"
            "and latest to access the most recently reported glucose measurement.",
            DeprecationWarning,
        )
        patient_id = coerce_patient_id(patient_identifier)

        response_json = self._get_graph_data_json(patient_id)

        return GraphResponse.model_validate(response_json)

    @authenticated
    def graph(
        self, patient_identifier: UUID | str | Patient
    ) -> list[GlucoseMeasurement]:
        """Requests and returns glucose measurements used to display graph data. Returns approximately the last 12 hours of data."""
        patient_id = coerce_patient_id(patient_identifier)

        response_json = self._get_graph_data_json(patient_id)

        return GraphResponse.model_validate(response_json).history

    @authenticated
    def latest(self, patient_identifier: UUID | str | Patient) -> GlucoseMeasurement:
        """Requests and returns the most recent glucose measurement"""
        patient_id = coerce_patient_id(patient_identifier)

        response_json = self._get_graph_data_json(patient_id)

        return GraphResponse.model_validate(response_json).current

    @authenticated
    def logbook(
        self, patient_identifier: UUID | str | Patient
    ) -> list[GlucoseMeasurement]:
        """Requests and returns patient logbook data, containing the measurements associated with glucose events for approximately the last 14 days."""
        patient_id = coerce_patient_id(patient_identifier)

        response_json = self._get_logbook_json(patient_id)

        return LogbookResponse.model_validate(response_json).data
