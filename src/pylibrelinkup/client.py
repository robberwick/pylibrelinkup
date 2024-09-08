from __future__ import annotations

from uuid import UUID

import requests
from pydantic import ValidationError

from .api_url import APIUrl
from .exceptions import AuthenticationError, RedirectError
from .models.connection import ConnectionResponse
from .models.data import Patient
from .models.login import LoginArgs, LoginResponse


class Client:
    """Client class to request data from the LibreLinkUp API."""

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
        # to first accept terms.
        # Here we handle the first two cases.
        # TODO: Handle the case where the user needs to accept terms.
        try:
            data_dict = data.get("data", {})
            if data_dict.get("redirect", False):
                raise RedirectError(APIUrl.from_string(data_dict["region"]))
            else:
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

    def read(self, patient_id: UUID) -> ConnectionResponse:
        """Requests and returns patient data"""
        response_json = self._get_graph_data_json(patient_id)

        return ConnectionResponse.model_validate(response_json)
