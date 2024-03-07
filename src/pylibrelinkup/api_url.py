from __future__ import annotations

from enum import StrEnum
from typing import Type, cast


class APIUrl(StrEnum):
    EU = "https://api-eu.libreview.io"
    EU2 = "https://api-eu2.libreview.io"
    US = "https://api.libreview.io"

    @classmethod
    def from_string(cls: Type[APIUrl], value: str) -> APIUrl:
        for member in cls:
            if member.lower() == value.lower():
                return cast(APIUrl, member)
        raise ValueError(f"{value} is not a valid {cls.__name__}")
