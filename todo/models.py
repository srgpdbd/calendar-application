from django.db import models

from core.models.mixins import SoftDeleteModel


class ToDo(SoftDeleteModel):

    title = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    label = models.ForeignKey('labels.Label', null=True, blank=True, on_delete=models.SET_NULL)
    done = models.BooleanField(default=False)
    calendar = models.ForeignKey(
        'calendars.Calendar',
        related_name='todos',
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = "ToDo"
        verbose_name_plural = "ToDos"

    def __str__(self):
        return self.title
