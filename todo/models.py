from django.db import models

from core.models.mixins import SoftDeleteMixin


class ToDo(SoftDeleteMixin, models.Model):

    title = models.CharField(max_length=150)
    user = models.ForeignKey('auth.User', related_name='todos', on_delete=models.PROTECT)

    class Meta:
        verbose_name = "ToDo"
        verbose_name_plural = "ToDos"

    def __str__(self):
        return self.title
