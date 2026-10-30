from __future__ import annotations

from enum import StrEnum
from typing import Type, cast

__all__ = ["APIUrl"]


class APIUrl(StrEnum):
    """Known LibreLinkUp regional API hosts.

    Redirects are resolved from the regional map published by the LibreLinkUp API; these values are used
    as the default host and as a fallback when the map is unavailable or lacks a region.
    """

    EU = "https://api-eu.libreview.io"
    EU2 = "https://api-eu2.libreview.io"
    US = "https://api-us.libreview.io"
    AE = "https://api-ae.libreview.io"
    AP = "https://api-ap.libreview.io"
    AU = "https://api-au.libreview.io"
    CA = "https://api-ca.libreview.io"
    DE = "https://api-de.libreview.io"
    FR = "https://api-fr.libreview.io"
    JP = "https://api-jp.libreview.io"
    LA = "https://api-la.libreview.io"
    RU = "https://api.libreview.ru"

    @classmethod
    def from_string(cls: Type[APIUrl], value: str) -> APIUrl:
        member: APIUrl
        for member in cls:
            if member.name.lower() == value.lower():
                return cast(APIUrl, member)
        raise ValueError(f"{value} is not a valid {cls.__name__}")
