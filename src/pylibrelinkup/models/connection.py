from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)
from pydantic.alias_generators import to_camel

from .config import AlarmRules
from .data import GlucoseMeasurement
from .hardware import Sensor, PatientDevice, ActiveSensor

__all__ = ["ConnectionResponse"]


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
    glucose_measurement: GlucoseMeasurement
    glucose_item: GlucoseMeasurement
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
    graph_data: list[GlucoseMeasurement] = Field(alias="graphData")


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

    @property
    def current(self) -> GlucoseMeasurement:
        """Returns the current glucose measurement."""
        return self.data.connection.glucose_measurement

    @property
    def history(self) -> list[GlucoseMeasurement]:
        """Returns the historical glucose measurements."""
        return self.data.graph_data

    @property
    def raw(self):
        """Returns the raw JSON data returned by the API."""
        return self.data.model_dump_json()
