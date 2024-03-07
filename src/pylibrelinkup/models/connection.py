from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)
from pydantic.alias_generators import to_camel

from .config import AlarmRules
from .data import GlucoseItem
from .hardware import Sensor, PatientDevice, ActiveSensor


class Connection(BaseModel):
    """Connection class to store connection data."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    id: UUID
    patient_id: UUID
    country: str
    status: int
    first_name: str
    last_name: str
    target_low: int
    target_high: int
    uom: int
    sensor: Sensor
    alarm_rules: AlarmRules
    glucose_measurement: GlucoseItem
    glucose_item: GlucoseItem
    glucose_alarm: None
    patient_device: PatientDevice
    created: int


class Data(BaseModel):
    """Data class to store connection data."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    connection: Connection
    active_sensors: list[ActiveSensor] = Field(alias="activeSensors")
    graph_data: list[GlucoseItem] = Field(alias="graphData")


class Ticket(BaseModel):
    """TicketData class to store ticket data."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    token: str
    expires: int
    duration: int


class ConnectionResponse(BaseModel):
    """ConnectionResponse class to store API connection endpoint response."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    status: int
    data: Data
    ticket: Ticket
