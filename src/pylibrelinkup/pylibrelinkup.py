"""
This is the main interface for the PyLibreLinkUp package, where you can authenticate and request data from the LibreLinkUp API.

In order to authenticate, you will need to sign up for an account at https://www.librelinkup.com/ and use your email and password to authenticate.
"""

from __future__ import annotations

import hashlib
import warnings
from uuid import UUID

import requests
from pydantic import ValidationError
from requests import HTTPError

from . import LLUAPIRateLimitError
from .api_url import APIUrl
from .data_types import PatientIdentifier
from .decorators import authenticated
from .exceptions import (
    AuthenticationError,
    EmailVerificationError,
    PrivacyPolicyError,
    RedirectError,
    TermsOfUseError,
)
from .models.connection import GraphResponse, LogbookResponse
from .models.data import GlucoseMeasurement, GlucoseMeasurementWithTrend, Patient
from .models.login import LoginArgs, LoginResponse
from .utilities import coerce_patient_id

__all__ = ["PyLibreLinkUp"]


HEADERS: dict[str, str] = {
    "accept-encoding": "gzip",
    "cache-control": "no-cache",
    "connection": "Keep-Alive",
    "content-type": "application/json",
    "product": "llu.android",
    "version": "4.12.0",
}


class PyLibreLinkUp:
    """PyLibreLinkUp class to request data from the LibreLinkUp API."""

    email: str
    password: str
    token: str | None
    account_id_hash: str | None

    def __init__(self, email: str, password: str, api_url: APIUrl = APIUrl.US) -> None:
        """
        Constructor for the PyLibreLinkUp class.

        :param email: The email address for the LibreLinkUp account.
        :type email: str
        :param password: The password for the LibreLinkUp account.
        :type password: str
        :param api_url: The regional API URL to use. Defaults to US.
        :type api_url: APIUrl
        :return: None
        """
        self.login_args: LoginArgs = LoginArgs(email=email, password=password)
        self.email = email or ""
        self.password = password or ""
        self.token = None
        self.account_id_hash = None
        self.api_url: str = api_url.value

    def _call_api(self, url: str) -> dict:
        """Calls the LibreLinkUp API and returns the response

        :type url: str
        :rtype: object
        """
        r = requests.get(url=url, headers=self._get_headers())
        try:
            r.raise_for_status()
        except HTTPError as e:
            if e.response.status_code == 429:
                retry_after = e.response.headers.get("Retry-After", "Unknown")
                raise LLUAPIRateLimitError(
                    response_code=e.response.status_code,
                    message=f"Too many requests. Please try again later.",
                    retry_after=int(retry_after) if retry_after.isdigit() else None,
                )
            else:
                raise
        data = r.json()
        return data

    def _set_token(self, token: str):
        """Saves the token for future requests."""
        self.token = token

    def _set_account_id_hash(self, account_id: str):
        """Saves the account_id_hash for future requests."""
        self.account_id_hash = hashlib.sha256(account_id.encode()).hexdigest()

    def _get_graph_data_json(self, patient_id: UUID) -> dict:
        """Requests and returns patient graph data

        :param patient_id: UUID
        :return:
        """
        return self._call_api(url=f"{self.api_url}/llu/connections/{patient_id}/graph")

    def _get_headers(self) -> dict:
        """Returns the headers for the request."""
        headers = HEADERS.copy()
        if self.token:
            headers.update({"authorization": "Bearer " + self.token})
        if self.account_id_hash:
            headers.update({"account-id": self.account_id_hash})
        return headers

    def _get_logbook_json(self, patient_id: UUID) -> dict:
        """Requests and returns patient logbook data

        :param patient_id: UUID
        :return:
        """
        return self._call_api(
            url=f"{self.api_url}/llu/connections/{patient_id}/logbook"
        )

    def authenticate(self) -> None:
        """Authenticate with the LibreLinkUp API

        :rtype: None
        """
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
            case "verifyEmail":
                raise EmailVerificationError()

        try:
            login_response = LoginResponse.model_validate(data)
        except ValidationError:
            raise AuthenticationError("Invalid login credentials")
        self._set_token(login_response.data.authTicket.token)
        self._set_account_id_hash(login_response.data.user.id)

    def get_patients(self) -> list[Patient]:
        """Requests and returns patient data

        :return: A list of patients.
        :rtype: list[Patient]
        """
        data = self._call_api(url=f"{self.api_url}/llu/connections")
        return [Patient.model_validate(patient) for patient in data["data"]]

    @authenticated
    def read(self, patient_identifier: PatientIdentifier) -> GraphResponse:
        """
        .. deprecated:: 0.6.0 The read method is deprecated. Instead, please use the graph method for retrieving graph data,"
            "and latest to access the most recently reported glucose measurement

        Requests and returns patient data

        :param patient_identifier: PatientIdentifier : The identifier of the patient.
        :return: The patient data.
        :rtype: GraphResponse


        """
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
    def graph(self, patient_identifier: PatientIdentifier) -> list[GlucoseMeasurement]:
        """Requests and returns glucose measurements used to display graph data. Returns approximately the last 12 hours of data.

        :param patient_identifier: PatientIdentifier: The identifier of the patient.
        :return: A list of glucose measurements.
        :rtype: list[GlucoseMeasurement]
        """
        patient_id = coerce_patient_id(patient_identifier)

        response_json = self._get_graph_data_json(patient_id)

        return GraphResponse.model_validate(response_json).history

    @authenticated
    def latest(
        self, patient_identifier: PatientIdentifier
    ) -> GlucoseMeasurementWithTrend:
        """Requests and returns the most recent glucose measurement

        :param patient_identifier: PatientIdentifier: The identifier of the patient.
        :return: The most recent glucose measurement.
        :rtype: GlucoseMeasurementWithTrend
        """
        patient_id = coerce_patient_id(patient_identifier)

        response_json = self._get_graph_data_json(patient_id)

        return GraphResponse.model_validate(response_json).current

    @authenticated
    def logbook(
        self, patient_identifier: PatientIdentifier
    ) -> list[GlucoseMeasurement]:
        """Requests and returns patient logbook data, containing the measurements associated with glucose events for approximately the last 14 days.

        :param patient_identifier: PatientIdentifier: The identifier of the patient.
        :return: A list of glucose measurements.
        :rtype: list[GlucoseMeasurement]
        """
        patient_id = coerce_patient_id(patient_identifier)

        response_json = self._get_logbook_json(patient_id)

        return LogbookResponse.model_validate(response_json).data
