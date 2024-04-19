from django.db import models


class DynamicModelMetaData(models.Model):
    id = models.AutoField(primary_key=True)
    model_name = models.CharField(max_length=255, unique=True)
    fields = models.JSONField(null=True)
