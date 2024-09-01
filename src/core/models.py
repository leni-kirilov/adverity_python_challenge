from django.db import models


# Create your models here.
class DatasetManager(models.Manager):
    def create_dataset(self, filename, date_created):
        dataset = self.create(filename=filename, date_created=date_created)
        return dataset


class Dataset(models.Model):
    filename = models.CharField(max_length=100)
    date_created = models.DateTimeField()

    objects = DatasetManager()

    class Meta:
        app_label = 'core'
