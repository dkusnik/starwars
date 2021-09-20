from django.conf import settings
from django.db import models


class CSVFiles(models.Model):
    file = models.FileField(upload_to=settings.CSV_STORAGE_DIR)
    date = models.DateTimeField()
