from pydantic import Field

from .base import ConfigBaseModel
from .config import FixedLowAlarmValues

__all__ = ["Sensor", "PatientDevice", "ActiveSensor"]


class Sensor(ConfigBaseModel):
    """Sensor class to store sensor data."""

    device_id: str = Field(default="")
    sn: str = Field(default="")
    a: int = Field(default=0)
    w: int = Field(default=0)
    pt: int = Field(default=0)


class PatientDevice(ConfigBaseModel):
    """PatientDevice class to store device data."""

    did: str = Field(default="")
    dtid: int = Field(default=0)
    v: str = Field(default="")
    ll: int = Field(default=0)
    hl: int = Field(default=0)
    u: int = Field(default=0)
    fixed_low_alarm_values: FixedLowAlarmValues
    alarms: bool = Field(default=False)


class ActiveSensor(ConfigBaseModel):
    """ActiveSensor class to store active sensor data."""

    sensor: Sensor
    device: PatientDevice
