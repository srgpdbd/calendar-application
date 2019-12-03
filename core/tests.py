from django.test import TestCase
from hamcrest import assert_that, not_none, has_length

from model_mommy import mommy
from labels.models import Label
from todo.models import ToDo


class SoftDeleteModel(TestCase):

    def test_delete_soft_deleted_model(self):
        created = mommy.make('todo.ToDo', label=Label.objects.get(id=1))
        created.delete()
        assert_that(created.deleted_at, not_none())

    def test_soft_delete_queryset(self):
        created = mommy.make('todo.ToDo', label=Label.objects.get(id=1))
        qs = ToDo.objects.filter(id=created.id)
        qs.delete()
        assert_that(qs[0].deleted_at, not_none())

    def test_get_not_deleted_models(self):
        created = mommy.make('todo.ToDo', label=Label.objects.get(id=1))
        qs = ToDo.objects.filter(id=created.id)
        qs.delete()
        deleted_qs = ToDo.active.all()
        assert_that(deleted_qs, has_length(0))
