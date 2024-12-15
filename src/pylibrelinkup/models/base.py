from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class ConfigBaseModel(BaseModel):
    """Base class for all models. Provides common configuration."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )
