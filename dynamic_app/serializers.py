from rest_framework import serializers

from dynamic_app.models import DynamicModelMetaData
from dynamic_app.validators import validate_field_type


class DynamicFieldSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=100, validators=[validate_field_type])
    options = serializers.JSONField(required=False)


class DynamicTableSerializer(serializers.Serializer):
    model_name = serializers.CharField(max_length=100)
    fields = serializers.DictField(child=DynamicFieldSerializer())


class DynamicModelMetaDataSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = DynamicModelMetaData
        fields = ['id', 'model_name', 'fields']


def create_dynamic_serializer(model):
    # Define a serializer class dynamically based on the model's fields
    meta_class = type('Meta', (), {'model': model, 'fields': '__all__'})
    dynamic_serializer_class = type('DynamicModelSerializer', (serializers.ModelSerializer,), {'Meta': meta_class})
    return dynamic_serializer_class
