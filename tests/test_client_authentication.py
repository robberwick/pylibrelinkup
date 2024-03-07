import json

import pytest
import requests
import responses
from polyfactory.factories.pydantic_factory import ModelFactory

from pylibrelinkup.client import Client, AuthenticationError
from pylibrelinkup.api_url import APIUrl
from pylibrelinkup.models.connection import ConnectionResponse
from pylibrelinkup.models.data import Patient
from pylibrelinkup.models.login import (
    LoginResponse,
)


class LoginResponseFactory(ModelFactory[LoginResponse]):
    __model__ = LoginResponse


class ConnectionResponseFactory(ModelFactory[ConnectionResponse]):
    __model__ = ConnectionResponse


class PatientFactory(ModelFactory[Patient]):
    __model__ = Patient


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.mark.parametrize("api_url", APIUrl)
def test_authenticate_raises_error_on_incorrect_login(
    mocked_responses, api_url: APIUrl
):
    """Test that the authenticate method raises an error when the login fails."""
    mocked_responses.add(
        responses.POST,
        f"{api_url.value}/llu/auth/login",
        json={"not": "important"},
        status=200,
    )

    client = Client(email="parp", password="parp", api_url=api_url)

    with pytest.raises(AuthenticationError):
        client.authenticate()


@pytest.mark.parametrize("api_url", APIUrl)
def test_authenticate_sets_token_on_correct_login(mocked_responses, api_url: APIUrl):
    """Test that the authenticate method sets the token on a successful login."""
    response = LoginResponseFactory.build()
    response.data.authTicket.token = "parp"
    assert isinstance(response, LoginResponse)

    mocked_responses.add(
        responses.POST,
        f"{api_url.value}/llu/auth/login",
        json=json.loads(response.model_dump_json()),
        status=200,
    )

    client = Client(email="parp", password="parp", api_url=api_url)

    client.authenticate()

    assert client.token == "parp"


@pytest.mark.parametrize("api_url", APIUrl)
def test_authenticate_raises_error_on_invalid_response(
    mocked_responses, api_url: APIUrl
):
    """Test that the authenticate method raises an error on invalid response."""
    mocked_responses.add(
        responses.POST,
        f"{api_url.value}/llu/auth/login",
        json={"invalid": "response"},
        status=200,
    )

    client = Client(email="parp", password="parp", api_url=api_url)

    with pytest.raises(AuthenticationError):
        client.authenticate()


@pytest.mark.parametrize("api_url", APIUrl)
def test_authenticate_raises_error_on_http_error(mocked_responses, api_url: APIUrl):
    """Test that the authenticate method raises an error on HTTP error."""
    mocked_responses.add(
        responses.POST,
        f"{api_url.value}/llu/auth/login",
        json={"error": "Unauthorized"},
        status=401,
    )

    client = Client(email="parp", password="parp", api_url=api_url)

    with pytest.raises(requests.exceptions.HTTPError):
        client.authenticate()
