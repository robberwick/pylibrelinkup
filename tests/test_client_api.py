import pytest
import responses
from requests import HTTPError

from pylibrelinkup import LLUAPIRateLimitError
from tests.conftest import pylibrelinkup_client


def test_call_api_with_rate_limit_and_numeric_retry_after(
    mocked_responses, pylibrelinkup_client
):
    """Test that 429 responses with numeric Retry-After raise LLAAPIRateLimitError with correct retry value."""
    url = f"{pylibrelinkup_client.api_url}/test/endpoint"
    mocked_responses.add(responses.GET, url, status=429, headers={"Retry-After": "30"})

    pylibrelinkup_client.client.token = "test_token"

    with pytest.raises(LLUAPIRateLimitError) as exc_info:
        pylibrelinkup_client.client._call_api(url)

    assert exc_info.value.response_code == 429
    assert exc_info.value.retry_after == 30
    assert "Too many requests" in str(exc_info.value)


def test_call_api_with_rate_limit_and_non_numeric_retry_after(
    mocked_responses, pylibrelinkup_client
):
    """Test that 429 responses with non-numeric Retry-After set retry_after to None."""
    url = f"{pylibrelinkup_client.api_url}/test/endpoint"
    mocked_responses.add(
        responses.GET, url, status=429, headers={"Retry-After": "soon"}
    )

    pylibrelinkup_client.client.token = "test_token"

    with pytest.raises(LLUAPIRateLimitError) as exc_info:
        pylibrelinkup_client.client._call_api(url)

    assert exc_info.value.retry_after is None


def test_call_api_with_rate_limit_and_missing_retry_after(
    mocked_responses, pylibrelinkup_client
):
    """Test that 429 responses without Retry-After set retry_after to None."""
    url = f"{pylibrelinkup_client.api_url}/test/endpoint"
    mocked_responses.add(responses.GET, url, status=429)

    pylibrelinkup_client.client.token = "test_token"

    with pytest.raises(LLUAPIRateLimitError) as exc_info:
        pylibrelinkup_client.client._call_api(url)

    assert exc_info.value.retry_after is None


def test_call_api_with_other_http_errors(mocked_responses, pylibrelinkup_client):
    """Test that non-429 HTTP errors are re-raised as HTTPError."""
    url = f"{pylibrelinkup_client.api_url}/test/endpoint"
    mocked_responses.add(responses.GET, url, status=401)

    pylibrelinkup_client.client.token = "test_token"

    with pytest.raises(HTTPError) as exc_info:
        pylibrelinkup_client.client._call_api(url)

    assert exc_info.value.response.status_code == 401


def test_call_api_successful_response(mocked_responses, pylibrelinkup_client):
    """Test that successful API calls return JSON data."""
    url = f"{pylibrelinkup_client.api_url}/test/endpoint"
    expected_data = {"test": "data"}

    mocked_responses.add(responses.GET, url, json=expected_data, status=200)

    pylibrelinkup_client.client.token = "test_token"
    result = pylibrelinkup_client.client._call_api(url)

    assert result == expected_data
