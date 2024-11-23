"""
This is the main interface for the PyLibreLinkUp package, where you can authenticate and request data from the LibreLinkUp API.

In order to authenticate, you will need to sign up for an account at https://www.librelinkup.com/ and use your email and password to authenticate.
"""

from __future__ import annotations

import warnings
from uuid import UUID

import requests

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

    _HEADERS = {
        "accept-encoding": "gzip",
        "cache-control": "no-cache",
        "connection": "Keep-Alive",
        "content-type": "application/json",
        "product": "llu.android",
        "version": "4.7.0",
    }

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
        self.api_url: str = api_url.value

    def authenticate(self) -> None:
        """Authenticate with the LibreLinkUp API

        :rtype: None
        """
        r = requests.post(
            url=f"{self.api_url}/llu/auth/login",
            headers=self._HEADERS,
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
            self._HEADERS.update({"authorization": "Bearer " + self.token})

        except KeyError:
            raise AuthenticationError("Invalid login credentials")

    def _call_api(self, url: str = None) -> dict:
        """Calls the LibreLinkUp API and returns the response

        :type url: str
        :rtype: object
        """
        r = requests.get(url=url, headers=self._HEADERS)
        r.raise_for_status()
        data = r.json()
        return data

    def get_patients(self) -> list[Patient]:
        """Requests and returns patient data

        :return: A list of patients.
        :rtype: list[Patient]
        """
        data = self._call_api(url=f"{self.api_url}/llu/connections")
        return [Patient.model_validate(patient) for patient in data["data"]]

    def _get_graph_data_json(self, patient_id: UUID) -> dict:
        """Requests and returns patient graph data

        :param patient_id: UUID
        :return:
        """
        return self._call_api(url=f"{self.api_url}/llu/connections/{patient_id}/graph")

    def _get_logbook_json(self, patient_id: UUID) -> dict:
        """Requests and returns patient logbook data

        :param patient_id: UUID
        :return:
        """
        return self._call_api(
            url=f"{self.api_url}/llu/connections/{patient_id}/logbook"
        )

    @authenticated
    def read(self, patient_identifier: UUID | str | Patient) -> GraphResponse:
        """
        .. deprecated:: 0.6.0 The read method is deprecated. Instead, please use the graph method for retrieving graph data,"
            "and latest to access the most recently reported glucose measurement

        Requests and returns patient data

        :param patient_identifier: UUID | str | Patient : The identifier of the patient.
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
    def graph(
        self, patient_identifier: UUID | str | Patient
    ) -> list[GlucoseMeasurement]:
        """Requests and returns glucose measurements used to display graph data. Returns approximately the last 12 hours of data.

        :param patient_identifier: UUID | str | Patient: The identifier of the patient.
        :return: A list of glucose measurements.
        :rtype: list[GlucoseMeasurement]
        """
        patient_id = coerce_patient_id(patient_identifier)

        response_json = self._get_graph_data_json(patient_id)

        return GraphResponse.model_validate(response_json).history

    @authenticated
    def latest(self, patient_identifier: UUID | str | Patient) -> GlucoseMeasurement:
        """Requests and returns the most recent glucose measurement

        :param patient_identifier: UUID | str | Patient: The identifier of the patient.
        :return: The most recent glucose measurement.
        :rtype: GlucoseMeasurement
        """
        patient_id = coerce_patient_id(patient_identifier)

        response_json = self._get_graph_data_json(patient_id)

        return GraphResponse.model_validate(response_json).current

    @authenticated
    def logbook(
        self, patient_identifier: UUID | str | Patient
    ) -> list[GlucoseMeasurement]:
        """Requests and returns patient logbook data, containing the measurements associated with glucose events for approximately the last 14 days.

        :param patient_identifier: UUID | str | Patient: The identifier of the patient.
        :return: A list of glucose measurements.
        :rtype: list[GlucoseMeasurement]
        """
        patient_id = coerce_patient_id(patient_identifier)

        response_json = self._get_logbook_json(patient_id)

        return LogbookResponse.model_validate(response_json).data
