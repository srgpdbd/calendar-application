from django.db import models
from core.models.mixins import SoftDeleteModel


class Calendar(SoftDeleteModel):

    name = models.CharField(max_length=25)
    user = models.ForeignKey(to='auth.User', on_delete=models.PROTECT, related_name='calendars')

    def __str__(self):
        return self.name
