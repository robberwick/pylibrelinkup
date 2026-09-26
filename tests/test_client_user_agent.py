import pytest
import responses

from pylibrelinkup import APIUrl, PyLibreLinkUp
from tests.conftest import pylibrelinkup_client


def test_default_user_agent_is_none():
    client = PyLibreLinkUp(email="test@example.com", password="password")
    assert client.user_agent is None


def test_user_agent_set_via_constructor():
    ua = "Mozilla/5.0 (custom)"
    client = PyLibreLinkUp(email="test@example.com", password="password", user_agent=ua)
    assert client.user_agent == ua


def test_user_agent_set_directly():
    client = PyLibreLinkUp(email="test@example.com", password="password")
    client.user_agent = "MyApp/1.0"
    assert client.user_agent == "MyApp/1.0"


def test_headers_contain_no_user_agent_by_default():
    client = PyLibreLinkUp(email="test@example.com", password="password")
    headers = client._get_headers()
    assert "User-Agent" not in headers


def test_headers_contain_user_agent_when_set():
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    client = PyLibreLinkUp(email="test@example.com", password="password", user_agent=ua)
    headers = client._get_headers()
    assert headers["User-Agent"] == ua


def test_headers_contain_user_agent_when_set_directly():
    client = PyLibreLinkUp(email="test@example.com", password="password")
    client.user_agent = "MyCustomAgent/2.0"
    headers = client._get_headers()
    assert headers["User-Agent"] == "MyCustomAgent/2.0"


def test_user_agent_sent_in_api_call(mocked_responses, pylibrelinkup_client):
    """User-Agent header override is forwarded in actual HTTP requests."""
    ua = "Mozilla/5.0 (test)"
    pylibrelinkup_client.client.user_agent = ua
    pylibrelinkup_client.client.token = "test_token"

    url = f"{pylibrelinkup_client.api_url}/test/endpoint"
    mocked_responses.add(responses.GET, url, json={"status": 0}, status=200)

    pylibrelinkup_client.client._call_api(url)

    assert len(mocked_responses.calls) == 1
    assert mocked_responses.calls[0].request.headers["User-Agent"] == ua


def test_user_agent_not_in_headers_when_none(mocked_responses, pylibrelinkup_client):
    """No User-Agent override means the key is absent from the sent headers."""
    pylibrelinkup_client.client.token = "test_token"

    url = f"{pylibrelinkup_client.api_url}/test/endpoint"
    mocked_responses.add(responses.GET, url, json={"status": 0}, status=200)

    pylibrelinkup_client.client._call_api(url)

    assert "User-Agent" not in pylibrelinkup_client.client._get_headers()


def test_null_byte_in_user_agent_raises():
    with pytest.raises(ValueError, match="null bytes"):
        PyLibreLinkUp(
            email="test@example.com", password="password", user_agent="bad\x00value"
        )
