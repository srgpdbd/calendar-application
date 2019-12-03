from django.db import models
from core.models.mixins import SoftDeleteModel


class Label(SoftDeleteModel):

    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
