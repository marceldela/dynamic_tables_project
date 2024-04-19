from django.core.exceptions import ValidationError
from rest_framework import serializers

TYPES_MAP = {
    'CharField': str,
    'IntegerField': int,
    'BooleanField': bool,
}


def validate_field_type(value: str):
    """
    Check that the field type has a valid 'type'.
    """

    # List of allowed types
    allowed_types = ["CharField", "IntegerField", "BooleanField"]

    # Validate field type
    if value not in allowed_types:
        raise serializers.ValidationError(
            f"The type for each field should be one of {allowed_types}. Got '{value}' instead."
        )

    return value


def validate_fields(request_data, field_definitions):
    for field_name, field_data in request_data.items():
        if field_name not in field_definitions:
            raise ValidationError(f"Field '{field_name}' is not defined in the model.")

        field_definition = field_definitions[field_name]
        expected_type = field_definition['type']

        # Check if the provided value matches the expected type
        provided_value = field_data
        if not isinstance(provided_value, TYPES_MAP[expected_type]):
            raise ValidationError(
                f"Value '{provided_value}' for field '{field_name}' is not of type '{expected_type}'.")
