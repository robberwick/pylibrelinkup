from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from pylibrelinkup.models.data import H, F, Nd, Std, L

__all__ = ["AlarmRules", "FixedLowAlarmValues"]


class AlarmRules(BaseModel):
    """AlarmRules class to store alarm rules data."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    c: bool
    h: H
    f: F
    l: L
    nd: Nd
    p: int
    r: int
    std: Std


class FixedLowAlarmValues(BaseModel):
    """FixedLowAlarmValues class to store fixed alarm values."""

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )

    mgdl: int
    mmoll: float
