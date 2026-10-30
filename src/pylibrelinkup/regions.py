"""
Resolve LibreLinkUp regional API hosts.

When a login is redirected to another region, the host for that region is looked up in the
``regionalMap`` published by the LibreLinkUp config endpoint. The static APIUrl enum
is used as a fallback for regions missing from the map (e.g. ``ru``) or when the endpoint is
unreachable.
"""

from __future__ import annotations

import requests

from .api_url import APIUrl
from .exceptions import UnknownRegionError

__all__ = ["resolve_region_host"]

DIRECTORY_URL = "https://api.libreview.io"

# Any valid country code returns the same regionalMap, so a fixed one is used.
_CONFIG_COUNTRY = "DE"

_regional_hosts: dict[str, str] | None = None


def fetch_regional_hosts(headers: dict[str, str]) -> dict[str, str]:
    """Fetch the regional host map from the LibreLinkUp config endpoint.

    The map is fetched once and cached for the lifetime of the process.

    :param headers: The headers to send with the request.
    :return: A mapping of lowercase region code to API host, without a trailing slash.
    :rtype: dict[str, str]
    """
    global _regional_hosts
    if _regional_hosts is None:
        r = requests.get(
            url=f"{DIRECTORY_URL}/llu/config/country",
            params={"country": _CONFIG_COUNTRY},
            headers=headers,
            timeout=10,
        )
        r.raise_for_status()
        regional_map = r.json()["data"]["regionalMap"]
        _regional_hosts = {
            region.lower(): entry["lslApi"].rstrip("/")
            for region, entry in regional_map.items()
        }
    return _regional_hosts


def resolve_region_host(region: str, headers: dict[str, str]) -> str:
    """Return the API host for a region code returned by a login redirect.

    The host is taken from the API's regional map, falling back to APIUrl.

    :param region: The region code, e.g. ``"us"`` or ``"eu2"``.
    :param headers: The headers to send with the config request
    :return: The API host, without a trailing slash.
    :rtype: str
    :raises UnknownRegionError: If the region is in neither the regional map nor APIUrl.
    """
    try:
        host = fetch_regional_hosts(headers).get(region.lower())
    except (requests.RequestException, KeyError, TypeError, AttributeError, ValueError):
        host = None
    if host:
        return host

    try:
        return APIUrl.from_string(region).value
    except ValueError:
        raise UnknownRegionError(region)


def clear_regional_hosts_cache() -> None:
    """Clear the cached regional host map, so the next lookup fetches it again"""
    global _regional_hosts
    _regional_hosts = None
