from typing import Optional

from django.db import OperationalError, ProgrammingError
from rest_framework import status, generics
from rest_framework.response import Response

from dynamic_app.enums import ResponseStatuses
from dynamic_app.models import DynamicModelMetaData
from dynamic_app.serializers import DynamicTableSerializer, DynamicModelMetaDataSerializer
from dynamic_app.viewsets import dynamic_service


class DynamicModelMixin:

    @staticmethod
    def extract_model_data(validated_data: dict) -> tuple:
        model_name = validated_data['model_name']
        model_fields = validated_data['fields']

        return model_name, model_fields

    @staticmethod
    def create_and_register_model(model_name: str, model_fields: dict) -> Response:
        try:
            dynamic_service.create_and_register_model(model_name, model_fields)
        except OperationalError as e:
            return Response({'status': 'Failed to create model', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ProgrammingError as e:
            return Response({'status': 'Failed to create model due to programming error', 'error': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': 'Failed to create model', 'error': str(e)}, )

        dynamic_metadata = DynamicModelMetaData.objects.get(model_name=model_name)
        dynamic_metadata_serializer = DynamicModelMetaDataSerializer(dynamic_metadata)
        return Response({'status': f'Model {model_name} created.', 'model': dynamic_metadata_serializer.data},
                        status=status.HTTP_201_CREATED)

    @staticmethod
    def unregister_and_validate(
            dynamic_model_metadata: DynamicModelMetaData, new_fields: dict):
        try:
            dynamic_model_metadata = dynamic_service.unregister_model(dynamic_model_metadata, new_fields=new_fields)
        except Exception as e:
            return Response({'status': 'Failed to unregister model', 'error': str(e)},
                            status=status.HTTP_400_BAD_REQUEST), ResponseStatuses.ERROR

        return dynamic_model_metadata, ResponseStatuses.SUCCESS


class DynamicModelCreateView(generics.CreateAPIView, DynamicModelMixin):
    serializer_class = DynamicTableSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            model_name, model_fields = self.extract_model_data(serializer.validated_data)
            return self.create_and_register_model(model_name, model_fields)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DynamicModelUpdateView(generics.RetrieveUpdateAPIView, DynamicModelMixin):
    serializer_class = DynamicTableSerializer
    http_method_names = ['put']

    def update(self, request, *args, **kwargs):
        model_id = kwargs.get('model_id')
        try:
            dynamic_model_metadata = DynamicModelMetaData.objects.get(id=model_id)
        except DynamicModelMetaData.DoesNotExist:
            return Response({'status': 'Model not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            model_name, model_fields = self.extract_model_data(serializer.validated_data)

            unregister_response, response_status = self.unregister_and_validate(dynamic_model_metadata, new_fields=model_fields)
            if response_status == ResponseStatuses.ERROR:
                return unregister_response

            try:
                self.create_and_register_model(model_name, model_fields)
            except Exception as e:
                return Response({'status': 'Failed to create model', 'error': str(e)},)
            dynamic_metadata_serializer = DynamicModelMetaDataSerializer(dynamic_model_metadata)

            return Response({'status': f'Model {model_name} updated.', 'model': dynamic_metadata_serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
