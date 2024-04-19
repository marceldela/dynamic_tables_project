from unittest.mock import patch, Mock
from django.urls import reverse
from rest_framework import status
import pytest
from django.test import RequestFactory
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from dynamic_app.models import DynamicModelMetaData
from dynamic_app.views import DynamicModelCreateView, DynamicModelUpdateView


@pytest.mark.django_db
def test_dynamic_model_create_view():
    factory = RequestFactory()

    # Create request data
    data = {
        "model_name": "MyModel",
        "fields": {
            "field1": {
                "type": "CharField",
                "options": {"max_length": 100}
            },
            "field2": {
                "type": "IntegerField",
                "options": {
                    "default": 0
                }
            }
        }
    }

    # Create request
    request = factory.post(reverse('create_dynamic_model'), data, format='json')

    # Assign request to the view
    view = DynamicModelCreateView.as_view()

    # Process request
    response = view(request)

    # Check status code and response
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["status"] == f"Model {data['model_name']} created."
    assert "model" in response.data

@pytest.mark.django_db
def test_dynamic_model_update_view():
    factory = RequestFactory()
    view = DynamicModelUpdateView.as_view()

    # Assuming this Model and data already exists
    existing_model_id = 1
    existing_data = {
        "model_name": "ExistingModel",
        "fields": {
            "existing_field": {
                "type": "CharField",
                "options": {"max_length": 100}
            }
        }
    }

    # This would be our new data that we are sending in the PUT request
    new_data = {
        "model_name": "UpdatedModel",
        "fields": {
            "new_field": {
                "type": "CharField",
                "options": {"max_length": 80}
            },
            "another_new_field": {
                "type": "IntegerField",
                "options": {
                    "default": 0
                }
            }
        }
    }
    with patch.object(DynamicModelMetaData, 'objects', return_value=Mock(spec=DynamicModelMetaData(id=1))) as mock:
        request = factory.put(reverse('update_dynamic_model', kwargs={'model_id': existing_model_id}), new_data,
                              format='json')
        response = view(request, model_id=existing_model_id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == f"Model {new_data['model_name']} updated."
        assert "model" in response.data