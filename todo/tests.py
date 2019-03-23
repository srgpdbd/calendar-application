from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.authtoken.models import Token

from model_mommy import mommy
from hamcrest import assert_that, equal_to, has_length

from todo.models import ToDo
from todo.views import ToDoView


class IntegrationalTests(TestCase):

    def testToDoList(self):
        deleted_to_do = mommy.make(ToDo, deleted_at=timezone.now())
        not_deleted_to_do = mommy.make(ToDo)
        user = mommy.make(User)
        token = Token.objects.get_or_create(user=user)
        view = ToDoView.as_view()
        request = APIRequestFactory().get('/api/todos/', format='json')
        force_authenticate(request, user=user, token=user.auth_token)
        response = view(request=request)
        assert_that(response.data, has_length(1))
        assert_that(response.data[0]['title'], equal_to(not_deleted_to_do.title))

