from django.db import models

from django.utils import timezone


class SoftDeletionQuerySet(models.QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(deleted_at=timezone.now())


class ObjectsWithSoftDeleteManager(models.Manager):

    def get_queryset(self):
        return SoftDeletionQuerySet(self.model).all()


class NotDeletedManager(models.Manager):
    """Manage only objects with deleted=False"""
    def get_queryset(self):
        return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
