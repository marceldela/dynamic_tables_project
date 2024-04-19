"""
URL configuration for dynamic_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from dynamic_app.views import DynamicModelCreateView, DynamicModelUpdateView
from dynamic_app.viewsets import (
    DynamicModelRowViewSet,
    DynamicModelRowCreationViewSet
)

schema_view = get_schema_view(
   openapi.Info(
      title="Dynamic table API",
      default_version='v1',
      description="Home project for portfolio",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()

router.register(r'api/table/(?P<model_id>\d+)/rows', DynamicModelRowViewSet, basename='get_rows')
router.register(r'api/table/(?P<model_id>\d+)/row', DynamicModelRowCreationViewSet, basename='create_row')

urlpatterns = [
    *router.urls,
    path("admin/", admin.site.urls),
    path('api/table/', DynamicModelCreateView.as_view(), name="create_dynamic_model"),
    path('api/table/<int:model_id>/', DynamicModelUpdateView.as_view(), name="update_dynamic_model"),
    # Swagger URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
