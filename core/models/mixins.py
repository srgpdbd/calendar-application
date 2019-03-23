from django.db import models
from django.utils import timezone

from core.models.managers import NotDeletedManager, ObjectsWithSoftDeleteManager


class SoftDeleteMixin(models.Model):
    """Mix soft deletion from base"""

    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = ObjectsWithSoftDeleteManager()
    active = NotDeletedManager()

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        # recursively delete related objects that have self.id as their foreign key
        for related_deletable in self._meta.related_objects:
            kwargs = dict()
            kwargs[related_deletable.field.attname] = self.id
            referring_models = related_deletable.related_model.objects.filter(**kwargs)
            for model in referring_models:
                model.delete()
        return self.save()