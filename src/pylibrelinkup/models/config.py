from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from pylibrelinkup.models.data import F, H, L, Nd, Std

__all__ = ["AlarmRules", "FixedLowAlarmValues"]


class AlarmRules(BaseModel):
    """AlarmRules class to store alarm rules data."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    c: bool = Field(default=False)
    h: H
    f: F
    l: L
    nd: Nd
    p: int = Field(default=0)
    r: int = Field(default=0)
    std: Std


class FixedLowAlarmValues(BaseModel):
    """FixedLowAlarmValues class to store fixed alarm values."""

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )

    mgdl: int = Field(default=0)
    mmoll: float = Field(default=0.0)
