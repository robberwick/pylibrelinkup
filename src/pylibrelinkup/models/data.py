from datetime import UTC, datetime
from enum import IntEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel, to_pascal
from pydantic_core.core_schema import ValidationInfo

__all__ = [
    "Patient",
    "Trend",
    "GlucoseMeasurement",
    "GlucoseMeasurementTrend",
    "F",
    "L",
    "H",
    "Nd",
    "Std",
]


class Patient(BaseModel):
    """Patient class to store patient data."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    id: UUID
    patient_id: UUID
    first_name: str
    last_name: str

    def __repr__(self):
        return f"{self.first_name} {self.last_name}: {self.patient_id}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}: {self.patient_id}"


class Trend(IntEnum):
    DOWN_FAST: int = 1
    DOWN_SLOW: int = 2
    STABLE: int = 3
    UP_SLOW: int = 4
    UP_FAST: int = 5


class GlucoseMeasurement(BaseModel):
    """GlucoseMeasurement class to store glucose measurement data."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        alias_generator=to_pascal,
        populate_by_name=True,
        from_attributes=True,
    )

    factory_timestamp: datetime = Field(None)
    timestamp: datetime = Field(None)
    type: int = Field(default=0)
    value_in_mg_per_dl: float = Field(default=0.0)
    measurement_color: int = Field(default=0)
    glucose_units: int = Field(default=0)
    value: float = Field(default=0.0)
    is_high: bool = Field(alias="isHigh")
    is_low: bool = Field(alias="isLow")

    def __str__(self):
        return f"{self.timestamp}: {self.value}"

    @field_validator("timestamp", "factory_timestamp", mode="before")
    @classmethod
    def parse_timestamp(cls, v: str, info: ValidationInfo):
        if isinstance(v, str):
            datetime_value = datetime.strptime(v, "%m/%d/%Y %I:%M:%S %p")
        elif isinstance(v, datetime):
            datetime_value = v
        else:
            raise ValueError(
                f"Invalid type for {info.field_name}: {type(v)}. Expected str or datetime."
            )

        if info.field_name == "factory_timestamp":
            # factory_timestamp is in UTC
            datetime_value = datetime_value.replace(tzinfo=UTC)
        return datetime_value


class GlucoseMeasurementTrend(GlucoseMeasurement):
    trend_arrow: Trend

    def __str__(self):
        return f"{super().__str__()} {self.trend_arrow}"


class F(BaseModel):
    """F class to store F data."""

    model_config = ConfigDict(
        from_attributes=True,
    )

    th: int = Field(default=0)
    thmm: float = Field(default=0.0)
    d: int = Field(default=0)
    tl: int = Field(default=0)
    tlmm: float = Field(default=0.0)


class L(BaseModel):
    """L class to store L data."""

    model_config = ConfigDict(
        from_attributes=True,
    )

    th: int = Field(default=0)
    thmm: float = Field(default=0.0)
    d: int = Field(default=0)
    tl: int = Field(default=0)
    tlmm: float = Field(default=0.0)


class H(BaseModel):
    """H class to store H data."""

    model_config = ConfigDict(
        from_attributes=True,
    )

    th: int = Field(default=0)
    thmm: float = Field(default=0.0)
    d: int = Field(default=0)
    f: float = Field(default=0.0)


class Nd(BaseModel):
    """Nd class to store Nd data."""

    model_config = ConfigDict(
        from_attributes=True,
    )

    i: int = Field(default=0)
    r: int = Field(default=0)
    l: int = Field(default=0)


class Std(BaseModel):
    """Std class to store Std data."""

    ...
    model_config = ConfigDict(
        from_attributes=True,
    )
    sd: bool | None = Field(default=None)
