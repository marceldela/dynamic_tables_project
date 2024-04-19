from django.db import models

from dynamic_app.services import DynamicModelService


def test_create_dynamic_model():
    model_name = "TestModel"
    model_fields = {'name': models.CharField(max_length=100)}

    result_model = DynamicModelService.create_dynamic_model(model_name, model_fields)

    assert result_model.__name__ == model_name
    assert 'name' in [field.name for field in result_model._meta.fields]
    assert result_model._meta.get_field('name').get_internal_type() == 'CharField'
