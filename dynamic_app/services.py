from typing import Optional

from django.apps import apps
from django.db import models, connection
from django.db.models.base import ModelBase

from dynamic_app.models import DynamicModelMetaData


class DynamicModelService:
    @staticmethod
    def create_dynamic_model(model_name: str, model_fields: dict) -> type(models.Model):
        # create Meta class dynamically
        Meta = type('Meta', (), {'verbose_name': model_name, 'app_label': 'dynamic_app'})

        attrs = {'__module__': 'dynamic_app.models', 'Meta': Meta}
        attrs.update(model_fields)

        model = ModelBase(model_name, (models.Model,), attrs)

        return model

    @classmethod
    def create_and_register_model(cls, model_name: str, model_fields: dict, update: bool = False) -> Optional[models.Model]:
        field_mapping = {
            'CharField': models.CharField,
            'IntegerField': models.IntegerField,
            'BooleanField': models.BooleanField,
        }

        model_fields_serializable = model_fields.copy()
        model_fields = {
            name: field_mapping[type_info['type']](**type_info.get('options', {})) for name, type_info in
            model_fields.items()
        }
        dynamic_model = cls.create_dynamic_model(model_name, model_fields)

        # Dynamically create and register model
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(dynamic_model)

        if update:
            # We don't need to create new meta object in case of update
            return

        # Create metadata model
        DynamicModelMetaData.objects.create(model_name=model_name, fields=model_fields_serializable)
        return dynamic_model

    @staticmethod
    def unregister_model(dynamic_model_metadata: DynamicModelMetaData, new_fields: dict) -> DynamicModelMetaData:
        model = apps.get_model('dynamic_app', dynamic_model_metadata.model_name)
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(model)

        # Replace metadata model fields
        dynamic_model_metadata.fields = new_fields
        dynamic_model_metadata.save()

        return dynamic_model_metadata
