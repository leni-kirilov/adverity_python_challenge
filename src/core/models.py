from django.db import models


class Dataset(models.Model):
    filename = models.CharField(max_length=100)
    date_created = models.DateTimeField()

    class Meta:
        app_label = "core"
