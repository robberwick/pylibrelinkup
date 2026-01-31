from typing import get_origin

from pydantic import BaseModel, ConfigDict, model_validator
from pydantic.alias_generators import to_camel


class ConfigBaseModel(BaseModel):
    """Base class for all models. Provides common configuration.

    This base class automatically handles None values for list-type fields
    by converting them to empty lists during validation. This prevents
    ValidationErrors when the API returns None for fields expecting lists.

    Configuration:
        - Strip whitespace from strings
        - Generate camelCase aliases for fields
        - Allow population by field name or alias
        - Enable attribute-based initialization
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    @model_validator(mode="before")
    @classmethod
    def preprocess_data(cls, data):
        """Preprocess input data before validation.

        This validator runs before Pydantic's field validation and applies
        transformations to the input data to handle API inconsistencies and
        ensure consistent data structures.

        Current transformations:
            - List-type fields: Converts None values to empty lists

        Args:
            data: The input data dictionary (or other value) to validate

        Returns:
            The modified data dictionary with transformations applied,
            or the original data if not a dict
        """
        if not isinstance(data, dict):
            return data

        for field_name, field_info in cls.model_fields.items():
            if field_name in data and data[field_name] is None:
                # Check if the field type is a list
                origin = get_origin(field_info.annotation)
                if origin is list:
                    data[field_name] = []

        return data
