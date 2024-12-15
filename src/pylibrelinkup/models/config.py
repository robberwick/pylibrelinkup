from pydantic import Field

from pylibrelinkup.models.base import ConfigBaseModel
from pylibrelinkup.models.data import F, H, L, Nd, Std

__all__ = ["AlarmRules", "FixedLowAlarmValues"]


class AlarmRules(ConfigBaseModel):
    """AlarmRules class to store alarm rules data."""

    c: bool = Field(default=False)
    h: H
    f: F
    l: L
    nd: Nd
    p: int = Field(default=0)
    r: int = Field(default=0)
    std: Std


class FixedLowAlarmValues(ConfigBaseModel):
    """FixedLowAlarmValues class to store fixed alarm values."""

    mgdl: int = Field(default=0)
    mmoll: float = Field(default=0.0)
