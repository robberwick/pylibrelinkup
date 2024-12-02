import json
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from .config import AlarmRules
from .data import GlucoseMeasurement
from .hardware import ActiveSensor, PatientDevice, Sensor

__all__ = ["GraphResponse", "LogbookResponse"]


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
    country: str = Field(default="")
    status: int = Field(default=0)
    first_name: str = Field(default="")
    last_name: str = Field(default="")
    target_low: int = Field(default=0)
    target_high: int = Field(default=0)
    uom: int = Field(default=0)
    sensor: Sensor
    alarm_rules: AlarmRules
    glucose_measurement: GlucoseMeasurement
    glucose_item: GlucoseMeasurement
    glucose_alarm: None
    patient_device: PatientDevice
    created: int = Field(default=0)


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

    token: str = Field(default="")
    expires: int = Field(default=0)
    duration: int = Field(default=0)


class GraphResponse(BaseModel):
    """GraphResponse class to store API graph data endpoint response."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    status: int = Field(default=0)
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


class LogbookResponse(BaseModel):
    """LogbookResponse class to store API logbook data endpoint response."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    status: int
    data: list[GlucoseMeasurement]
    ticket: Ticket

    @property
    def raw(self):
        """Returns the raw JSON data returned by the API."""
        return json.dumps(
            [json.loads(measurement.model_dump_json()) for measurement in self.data]
        )
