import pytest
from django.core.exceptions import ValidationError
from rest_framework import serializers

from dynamic_app.validators import validate_field_type, validate_fields


def test_validate_field_type():
    # Test with valid data
    valid_data = ["CharField", "IntegerField", "BooleanField"]
    for field_type in valid_data:
        assert validate_field_type(field_type) == field_type

    # Test with invalid data
    invalid_data = ["InvalidField", "AnotherInvalidField", 123, None, True]
    for field_type in invalid_data:
        with pytest.raises(serializers.ValidationError):
            validate_field_type(field_type)

def test_validate_fields():
    field_definitions = {
        'field1': {'type': 'CharField'},
        'field2': {'type': 'IntegerField'},
        'field3': {'type': 'BooleanField'}
    }

    # Test with valid data
    valid_data = {
        'field1': 'text',
        'field2': 123,
        'field3': True
    }
    validate_fields(valid_data, field_definitions)

    # Test with invalid data
    invalid_data = {
        'field1': 123,  # Expected CharField, provided Integer
        'field2': 'text',  # Expected IntegerField, provided String
        'field4': True  # Field not defined in field_definitions
    }
    with pytest.raises(ValidationError):
        validate_fields(invalid_data, field_definitions)
