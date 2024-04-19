import pytest
from rest_framework import serializers

from dynamic_app.validators import validate_field_type, validate_field, validate_json


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


def test_validate_field():
    with pytest.raises(TypeError):
        validate_field("test", "int")  # Should raise error as "test" is not of type int
    assert validate_field("test", "str") is None  # Should return None as "test" is a string
    with pytest.raises(TypeError):
        validate_field("test", "bool")  # Should raise error as "test" is not of type bool


def test_validate_json():
    json_data = {"age": 21, "name": "John", "is_student": False}
    schema = {"age": "int", "name": "str", "is_student": "bool"}
    assert validate_json(json_data, schema) is None  # Should return None as json_data fits the schema

    wrong_schema = {"age": "str", "name": "str", "is_student": "int"}
    assert validate_json(json_data,
                         wrong_schema) == "Incorrect type for field. Expected <class 'str'>, got <class 'int'>"
