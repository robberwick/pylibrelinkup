import json

import pytest
import requests
import responses

from pylibrelinkup import (
    PyLibreLinkUp,
    APIUrl,
    AuthenticationError,
    TermsOfUseError,
    RedirectError,
)
from pylibrelinkup.exceptions import PrivacyPolicyError
from pylibrelinkup.models.login import (
    LoginResponse,
)
from tests.conftest import mocked_responses, pylibrelinkup_client
from tests.factories import LoginResponseFactory


def test_client_uses_correct_api_url_default():
    """Test that the client uses the correct API URL by default."""
    client = PyLibreLinkUp(email="parp", password="parp")
    assert client.api_url == APIUrl.US.value


def test_authenticate_raises_error_on_incorrect_login(
    mocked_responses, pylibrelinkup_client
):
    """Test that the authenticate method raises an error when the login fails."""
    mocked_responses.add(
        responses.POST,
        f"{pylibrelinkup_client.api_url.value}/llu/auth/login",
        json={"not": "important"},
        status=200,
    )

    with pytest.raises(AuthenticationError):
        pylibrelinkup_client.client.authenticate()


def test_authenticate_sets_token_on_correct_login(
    mocked_responses, pylibrelinkup_client
):
    """Test that the authenticate method sets the token on a successful login."""
    response = LoginResponseFactory.build()
    response.data.authTicket.token = "parp"
    assert isinstance(response, LoginResponse)

    mocked_responses.add(
        responses.POST,
        f"{pylibrelinkup_client.api_url.value}/llu/auth/login",
        json=json.loads(response.model_dump_json()),
        status=200,
    )

    pylibrelinkup_client.client.authenticate()

    assert pylibrelinkup_client.client.token == "parp"


def test_authenticate_raises_error_on_invalid_response(
    mocked_responses, pylibrelinkup_client
):
    """Test that the authenticate method raises an error on invalid response."""
    mocked_responses.add(
        responses.POST,
        f"{pylibrelinkup_client.api_url.value}/llu/auth/login",
        json={"invalid": "response"},
        status=200,
    )

    with pytest.raises(AuthenticationError):
        pylibrelinkup_client.client.authenticate()


def test_authenticate_raises_error_on_http_error(
    mocked_responses, pylibrelinkup_client
):
    """Test that the authenticate method raises an error on HTTP error."""
    mocked_responses.add(
        responses.POST,
        f"{pylibrelinkup_client.api_url.value}/llu/auth/login",
        json={"error": "Unauthorized"},
        status=401,
    )

    with pytest.raises(requests.exceptions.HTTPError):
        pylibrelinkup_client.client.authenticate()


def test_authenticate_raises_terms_of_use_error(
    mocked_responses, pylibrelinkup_client, terms_of_use_response_json
):
    """Test that the authenticate method raises a TermsOfUseError, when the user needs to accept terms of use."""

    mocked_responses.add(
        responses.POST,
        f"{pylibrelinkup_client.api_url.value}/llu/auth/login",
        json=terms_of_use_response_json,
        status=200,
    )

    with pytest.raises(TermsOfUseError):
        pylibrelinkup_client.client.authenticate()


def test_authenticate_raises_privacy_policy_error(
    mocked_responses, pylibrelinkup_client, privacy_policy_response_json
):
    """Test that the authenticate method raises a PrivacyPolicyError, when the user needs to accept the privacy policy."""

    mocked_responses.add(
        responses.POST,
        f"{pylibrelinkup_client.api_url.value}/llu/auth/login",
        json=privacy_policy_response_json,
        status=200,
    )

    with pytest.raises(PrivacyPolicyError):
        pylibrelinkup_client.client.authenticate()


def test_redirection_response_raises_redirect_error(
    mocked_responses, pylibrelinkup_client, redirect_response_json
):
    """Test that the authenticate method raises a RedirectError, when the user is redirected to a different region."""

    mocked_responses.add(
        responses.POST,
        f"{pylibrelinkup_client.api_url.value}/llu/auth/login",
        json=redirect_response_json,
        status=200,
    )

    with pytest.raises(RedirectError):
        pylibrelinkup_client.client.authenticate()
