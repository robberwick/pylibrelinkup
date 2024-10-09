from pydantic import BaseModel, ConfigDict
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

    device_id: str
    sn: str
    a: int
    w: int
    pt: int


class PatientDevice(BaseModel):
    """PatientDevice class to store device data."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    did: str
    dtid: int
    v: str
    ll: int
    hl: int
    u: int
    fixed_low_alarm_values: FixedLowAlarmValues
    alarms: bool


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
