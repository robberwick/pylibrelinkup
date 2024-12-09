from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from .config import FixedLowAlarmValues

__all__ = ["Sensor", "PatientDevice", "ActiveSensor"]


class Sensor(BaseModel):
    """Sensor class to store sensor data."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    device_id: str = Field(default="")
    sn: str = Field(default="")
    a: int = Field(default=0)
    w: int = Field(default=0)
    pt: int = Field(default=0)


class PatientDevice(BaseModel):
    """PatientDevice class to store device data."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    did: str = Field(default="")
    dtid: int = Field(default=0)
    v: str = Field(default="")
    ll: int = Field(default=0)
    hl: int = Field(default=0)
    u: int = Field(default=0)
    fixed_low_alarm_values: FixedLowAlarmValues
    alarms: bool = Field(default=False)


class ActiveSensor(BaseModel):
    """ActiveSensor class to store active sensor data."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    sensor: Sensor
    device: PatientDevice
