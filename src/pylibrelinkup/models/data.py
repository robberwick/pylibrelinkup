from datetime import UTC, datetime
from enum import IntEnum
from uuid import UUID

from pydantic import ConfigDict, Field, field_validator
from pydantic.alias_generators import to_pascal
from pydantic_core.core_schema import ValidationInfo

__all__ = [
    "Patient",
    "Trend",
    "GlucoseMeasurement",
    "GlucoseMeasurementWithTrend",
    "F",
    "L",
    "H",
    "Nd",
    "Std",
]

from pylibrelinkup.models.base import ConfigBaseModel


class Patient(ConfigBaseModel):
    """Patient class to store patient data."""

    id: UUID
    patient_id: UUID
    first_name: str
    last_name: str

    def __repr__(self):
        return f"{self.first_name} {self.last_name}: {self.patient_id}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}: {self.patient_id}"


class Trend(IntEnum):
    DOWN_FAST = 1
    DOWN_SLOW = 2
    STABLE = 3
    UP_SLOW = 4
    UP_FAST = 5

    @property
    def indicator(self) -> str:
        arrow_map: dict[Trend, str] = {
            Trend.DOWN_FAST: "↓",
            Trend.DOWN_SLOW: "↘",
            Trend.STABLE: "→",
            Trend.UP_SLOW: "↗",
            Trend.UP_FAST: "↑",
        }
        return arrow_map[self]


class GlucoseMeasurement(ConfigBaseModel):
    """GlucoseMeasurement class to store glucose measurement data."""

    # Glucose measurements _mostly_ use PascalCase, instead of camelCase because
    # ¯\_(ツ)_/¯
    model_config = ConfigDict(
        alias_generator=to_pascal,
    )

    factory_timestamp: datetime
    timestamp: datetime
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


class F(ConfigBaseModel):
    """F class to store F data."""

    th: int = Field(default=0)
    thmm: float = Field(default=0.0)
    d: int = Field(default=0)
    tl: int = Field(default=0)
    tlmm: float = Field(default=0.0)


class L(ConfigBaseModel):
    """L class to store L data."""

    th: int = Field(default=0)
    thmm: float = Field(default=0.0)
    d: int = Field(default=0)
    tl: int = Field(default=0)
    tlmm: float = Field(default=0.0)


class H(ConfigBaseModel):
    """H class to store H data."""

    th: int = Field(default=0)
    thmm: float = Field(default=0.0)
    d: int = Field(default=0)
    f: float = Field(default=0.0)


class Nd(ConfigBaseModel):
    """Nd class to store Nd data."""

    i: int = Field(default=0)
    r: int = Field(default=0)
    l: int = Field(default=0)


class Std(ConfigBaseModel):
    """Std class to store Std data."""

    sd: bool | None = Field(default=None)


class GlucoseMeasurementWithTrend(GlucoseMeasurement):
    trend: Trend = Field(default=Trend.STABLE, alias="TrendArrow")
