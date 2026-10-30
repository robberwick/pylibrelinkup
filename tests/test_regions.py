import pytest
import responses

from pylibrelinkup import APIUrl, PyLibreLinkUp, RedirectError, UnknownRegionError
from pylibrelinkup.regions import DIRECTORY_URL

CONFIG_URL = f"{DIRECTORY_URL}/llu/config/country"


def redirect_response_json(region: str) -> dict:
    """Return a login response redirecting to the given region."""
    return {"data": {"redirect": True, "region": region}, "status": 0}


def test_redirect_resolves_host_from_regional_map(mocked_responses, get_response_json):
    """Test that a redirect resolves the region's host from the config endpoint's regional map."""
    client = PyLibreLinkUp(email="parp", password="parp")
    mocked_responses.add(
        responses.POST,
        f"{client.api_url}/llu/auth/login",
        json=get_response_json("redirect_response.json"),  # region "eu2"
    )
    mocked_responses.add(
        responses.GET,
        CONFIG_URL,
        json=get_response_json("country_config_response.json"),
    )

    with pytest.raises(RedirectError) as exc_info:
        client.authenticate()

    assert exc_info.value.region_code == "eu2"
    assert exc_info.value.api_url == "https://api-eu2.libreview.io"
    assert exc_info.value.region == APIUrl.EU2


def test_redirect_to_region_missing_from_api_url_uses_regional_map(
    mocked_responses, get_response_json
):
    """Test that a region present in the regional map but absent from APIUrl resolves without error."""
    client = PyLibreLinkUp(email="parp", password="parp")
    mocked_responses.add(
        responses.POST,
        f"{client.api_url}/llu/auth/login",
        json=redirect_response_json("xx"),
    )
    mocked_responses.add(
        responses.GET,
        CONFIG_URL,
        json=get_response_json("country_config_response.json"),
    )

    with pytest.raises(RedirectError) as exc_info:
        client.authenticate()

    assert exc_info.value.region_code == "xx"
    assert exc_info.value.api_url == "https://api-xx.libreview.io"
    assert exc_info.value.region is None


def test_redirect_to_region_missing_from_regional_map_falls_back_to_api_url(
    mocked_responses, get_response_json
):
    """Test that a region absent from the regional map (e.g. ru) falls back to APIUrl."""
    client = PyLibreLinkUp(email="parp", password="parp")
    mocked_responses.add(
        responses.POST,
        f"{client.api_url}/llu/auth/login",
        json=redirect_response_json("ru"),
    )
    mocked_responses.add(
        responses.GET,
        CONFIG_URL,
        json=get_response_json("country_config_response.json"),
    )

    with pytest.raises(RedirectError) as exc_info:
        client.authenticate()

    assert exc_info.value.api_url == APIUrl.RU.value
    assert exc_info.value.region == APIUrl.RU


def test_redirect_falls_back_to_api_url_when_config_endpoint_fails(
    mocked_responses, get_response_json
):
    """Test that a failing config endpoint falls back to APIUrl."""
    client = PyLibreLinkUp(email="parp", password="parp")
    mocked_responses.add(
        responses.POST,
        f"{client.api_url}/llu/auth/login",
        json=get_response_json("redirect_response.json"),  # region "eu2"
    )
    mocked_responses.add(responses.GET, CONFIG_URL, status=500)

    with pytest.raises(RedirectError) as exc_info:
        client.authenticate()

    assert exc_info.value.api_url == APIUrl.EU2.value


def test_redirect_to_unknown_region_raises_unknown_region_error(
    mocked_responses, get_response_json
):
    """Test that a region in neither the regional map nor APIUrl raises UnknownRegionError."""
    client = PyLibreLinkUp(email="parp", password="parp")
    mocked_responses.add(
        responses.POST,
        f"{client.api_url}/llu/auth/login",
        json=redirect_response_json("zz"),
    )
    mocked_responses.add(
        responses.GET,
        CONFIG_URL,
        json=get_response_json("country_config_response.json"),
    )

    with pytest.raises(UnknownRegionError) as exc_info:
        client.authenticate()

    assert exc_info.value.region == "zz"


def test_regional_map_is_fetched_once(mocked_responses, get_response_json):
    """Test that the regional map is cached after the first redirect."""
    client = PyLibreLinkUp(email="parp", password="parp")
    mocked_responses.add(
        responses.POST,
        f"{client.api_url}/llu/auth/login",
        json=get_response_json("redirect_response.json"),  # region "eu2"
    )
    mocked_responses.add(
        responses.GET,
        CONFIG_URL,
        json=get_response_json("country_config_response.json"),
    )

    for _ in range(2):
        with pytest.raises(RedirectError):
            client.authenticate()

    config_calls = [
        call
        for call in mocked_responses.calls
        if call.request.url.startswith(CONFIG_URL)
    ]
    assert len(config_calls) == 1


def test_client_accepts_api_url_string_and_strips_trailing_slash():
    """Test that the client accepts a host string, such as RedirectError.api_url."""
    client = PyLibreLinkUp(
        email="parp", password="parp", api_url="https://api-xx.libreview.io/"
    )
    assert client.api_url == "https://api-xx.libreview.io"
