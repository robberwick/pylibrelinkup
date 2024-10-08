import json

import pytest
import requests
import responses

from pylibrelinkup import PyLibreLinkUp, APIUrl, AuthenticationError, TermsOfUseError
from pylibrelinkup.models.login import (
    LoginResponse,
)
from tests.conftest import mocked_responses
from tests.factories import LoginResponseFactory


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

    client = PyLibreLinkUp(email="parp", password="parp", api_url=api_url)

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

    client = PyLibreLinkUp(email="parp", password="parp", api_url=api_url)

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

    client = PyLibreLinkUp(email="parp", password="parp", api_url=api_url)

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

    client = PyLibreLinkUp(email="parp", password="parp", api_url=api_url)

    with pytest.raises(requests.exceptions.HTTPError):
        client.authenticate()


@pytest.mark.parametrize("api_url", APIUrl)
def test_authenticate_raises_terms_of_use_error(
    mocked_responses, api_url: APIUrl, terms_of_use_response_json
):
    """Test that the authenticate method raises a TermsOfUseError, when the user needs to accept terms of use."""

    mocked_responses.add(
        responses.POST,
        f"{api_url.value}/llu/auth/login",
        json=terms_of_use_response_json,
        status=200,
    )

    client = PyLibreLinkUp(email="parp", password="parp", api_url=api_url)

    with pytest.raises(TermsOfUseError):
        client.authenticate()
