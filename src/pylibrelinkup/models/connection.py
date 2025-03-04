import json
from typing import Any, Self
from uuid import UUID

from pydantic import Field, ValidationError, model_validator
from pydantic.functional_validators import ModelWrapValidatorHandler

from .base import ConfigBaseModel
from .config import AlarmRules
from .data import GlucoseMeasurement, GlucoseMeasurementWithTrend
from .hardware import ActiveSensor, PatientDevice, Sensor

__all__ = ["GraphResponse", "LogbookResponse"]

from ..exceptions import PatientNotFoundError


class Connection(ConfigBaseModel):
    """Connection class to store connection data."""

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
    glucose_measurement: GlucoseMeasurementWithTrend = Field(alias="glucoseMeasurement")
    glucose_item: GlucoseMeasurement
    glucose_alarm: None
    patient_device: PatientDevice
    created: int = Field(default=0)


class Data(ConfigBaseModel):
    """Data class to store connection data."""

    connection: Connection
    active_sensors: list[ActiveSensor] = Field(alias="activeSensors")
    graph_data: list[GlucoseMeasurement] = Field(alias="graphData")


class Ticket(ConfigBaseModel):
    """TicketData class to store ticket data."""

    token: str = Field(default="")
    expires: int = Field(default=0)
    duration: int = Field(default=0)


class APIResponse(ConfigBaseModel):
    """Base model for API responses."""

    status: int = Field(default=0)
    ticket: Ticket

    @property
    def raw(self):
        """Returns the raw JSON data returned by the API."""
        return self.data.model_dump_json()

    @model_validator(mode="wrap")
    @classmethod
    def validate_api_response(
        cls, data: Any, handler: ModelWrapValidatorHandler[Self]
    ) -> Self:
        try:
            return handler(data)
        except ValidationError:
            # TODO: Add logging
            # TODO: Extend this to handle other exceptions e.g. redirections, terms of use, etc.
            # if the data is a dictionary, and it should contain an "error" and "status" key
            # match against the status to determine what exception to raise
            # if there's no match, raise the original exception
            if isinstance(data, dict):
                match data:
                    case {
                        "status": 4
                    }:  # 4 is the status code for "couldNotLoadPatient"
                        raise PatientNotFoundError()
            # No match, raise the original exception
            raise


class GraphResponse(APIResponse):
    """GraphResponse class to store API graph data endpoint response."""

    data: Data

    @property
    def current(self) -> GlucoseMeasurementWithTrend:
        """Returns the current glucose measurement."""
        return self.data.connection.glucose_measurement

    @property
    def history(self) -> list[GlucoseMeasurement]:
        """Returns the historical glucose measurements."""
        return self.data.graph_data


class LogbookResponse(APIResponse):
    """LogbookResponse class to store API logbook data endpoint response."""

    data: list[GlucoseMeasurement]

    @property
    def raw(self):
        """Returns the raw JSON data returned by the API."""
        return json.dumps(
            [json.loads(measurement.model_dump_json()) for measurement in self.data]
        )
