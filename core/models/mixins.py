from django.db import models
from django.utils import timezone

from core.models.managers import NotDeletedManager, ObjectsWithSoftDeleteManager


class SoftDeleteModel(models.Model):
    """Mix soft deletion from base"""

    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = ObjectsWithSoftDeleteManager()
    active = NotDeletedManager()

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        return self.save()
