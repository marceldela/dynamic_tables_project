import pytest
from django.test import RequestFactory
from django.urls import reverse
from rest_framework import status

from dynamic_app.views import DynamicModelCreateView


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
