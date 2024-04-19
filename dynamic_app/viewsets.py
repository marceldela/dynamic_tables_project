from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from dynamic_app.models import DynamicModelMetaData
from dynamic_app.serializers import create_dynamic_serializer
from dynamic_app.services import DynamicModelService
from dynamic_app.validators import validate_fields

dynamic_service = DynamicModelService


def get_model_metadata(model_id):
    """
    Get the DynamicModelMetaData from the database
    """
    try:
        return DynamicModelMetaData.objects.get(id=model_id)
    except ObjectDoesNotExist:
        return None


class DynamicModelRowViewSet(generics.ListAPIView, GenericViewSet):

    def get_queryset(self):
        model_id = self.kwargs['model_id']
        dynamic_model_metadata = get_model_metadata(model_id)

        if not dynamic_model_metadata:
            return Response(status=status.HTTP_404_NOT_FOUND)

        model = apps.get_model('dynamic_app', dynamic_model_metadata.model_name)
        rows = model.objects.all()
        return rows

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        model_class = queryset.model

        serializer_class = create_dynamic_serializer(model=model_class)

        serializer = serializer_class(queryset, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class DynamicModelRowCreationViewSet(generics.CreateAPIView, GenericViewSet):

    def create(self, request, *args, **kwargs):
        model_id = kwargs.get('model_id')
        dynamic_model_metadata = get_model_metadata(model_id)

        if not dynamic_model_metadata:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Validate request data with the metadata schema
        try:
            validate_fields(request.data.get('fields'), dynamic_model_metadata.fields)
        except ValidationError as e:
            return Response(e.messages, status=status.HTTP_400_BAD_REQUEST)

        # Save data
        model = apps.get_model(app_label='dynamic_app', model_name=dynamic_model_metadata.model_name)

        instance = model.objects.create(**request.data['fields'])
        serializer_class = create_dynamic_serializer(model=model)
        serializer = serializer_class(instance)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)
