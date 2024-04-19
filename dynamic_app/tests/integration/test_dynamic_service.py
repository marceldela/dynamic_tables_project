import pytest
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from django.db import ProgrammingError

from dynamic_app.models import DynamicModelMetaData
from dynamic_app.services import DynamicModelService


@pytest.mark.django_db
def test_create_and_register_model():
    model_fields = {
        'name': {
            'type': 'CharField',
            'options': {
                'max_length': 100
            }
        }
    }
    model_name = "TestModel"
    dynamic_model = DynamicModelService.create_and_register_model(model_name, model_fields)
    try:
        dynamic_model_db = apps.get_model('dynamic_app', model_name)
    except ImproperlyConfigured:
        dynamic_model_db = None

    assert dynamic_model_db is not None, "Model registration failed"
    assert dynamic_model == dynamic_model_db, "Models do not match"
    assert DynamicModelMetaData.objects.filter(model_name=model_name, fields=model_fields).exists()
