from model_mommy import mommy
from hamcrest import assert_that, equal_to, has_length
from django.contrib.auth import get_user_model
from django.utils import timezone
from graphql_jwt.testcases import JSONWebTokenTestCase
from datetime import datetime

from todo.schema import ToDoQuery
from todo.models import ToDo


class Queries(JSONWebTokenTestCase):

    def setUp(self):
        self.query = ToDoQuery().resolve_todos
        self.default_user = mommy.make(get_user_model())
        self.client.authenticate(self.default_user)
        self.calendar = mommy.make('calendars.Calendar', id=1, user=self.default_user)
        self.valid_query = f'''
            {{
                todos(calendarId: {self.calendar.id}) {{
                    id
                }}
            }}'''

    def test_get_all_todos_with_one_todo(self):
        new_todo = mommy.make('todo.ToDo', calendar=self.calendar, )
        result = self.client.execute(self.valid_query, variables={'calendar_id': self.calendar.id}).to_dict()
        todos = result['data']['todos']

        assert_that(todos, has_length(1))
        assert_that(todos[0]['id'], equal_to(str(new_todo.id)))

    def test_get_all_todos_with_several_todos(self):
        todos_to_create = 12
        mommy.make('todo.ToDo', calendar=self.calendar, _quantity=todos_to_create)
        result = self.client.execute(self.valid_query, variables={'calendar_id': self.calendar.id}).to_dict()
        todos = result['data']['todos']
        created_todo_ids = [int(todo['id']) for todo in todos]
        existed_todo_ids = list(ToDo.objects.filter(calendar=self.calendar).values_list('id', flat=True))

        assert_that(todos, has_length(todos_to_create))
        assert_that(set(existed_todo_ids), equal_to(set(created_todo_ids)))

    def test_get_all_todos_with_different_calendars(self):
        todos_to_create = 12
        mommy.make('todo.ToDo', calendar=self.calendar, _quantity=todos_to_create)
        query = f'''
            {{
                todos(calendarId: 2) {{
                    id
                }}
            }}'''
        result = self.client.execute(query, variables={'calendar_id': self.calendar.id}).to_dict()
        valid_result = self.client.execute(self.valid_query, variables={'calendar_id': self.calendar.id}).to_dict()
        todos = result['data']['todos']
        valid_result_todos = valid_result['data']['todos']

        assert_that(todos, has_length(0))
        assert_that(valid_result_todos, has_length(todos_to_create))

    def test_get_todos_by_specific_date(self):
        date_string = "1990-01-01"
        date_for_todo = datetime.strptime(date_string, "%Y-%m-%d")
        date_dor_not_valid_todo = timezone.now()
        new_todo = mommy.make('todo.ToDo', calendar=self.calendar, date=timezone.make_aware(date_for_todo))
        not_valid = mommy.make('todo.ToDo', calendar=self.calendar, date=date_dor_not_valid_todo)
        without_date = mommy.make('todo.ToDo', calendar=self.calendar,)
        query = f'''
            {{
                todos(calendarId: {self.calendar.id}, date: "{date_string}") {{
                    id
                }}
            }}'''
        result = self.client.execute(query, variables={'calendar_id': self.calendar.id}).to_dict()
        todos = result['data']['todos']
        assert_that(todos, has_length(1))
        all_todo_ids = [todo['id'] for todo in todos]

        assert_that(todos[0]['id'], equal_to(str(new_todo.id)))
        assert_that(not_valid.id not in all_todo_ids, equal_to(True))
        assert_that(without_date.id not in all_todo_ids, equal_to(True))


class Mutations(JSONWebTokenTestCase):

    def test_create_todo_without_mandatory_params(self):
        pass

    def test_create_todo_with_mandatory_params(self):
        pass

    def test_create_todo_with_fields_that_not_present_in_todo_model(self):
        pass

    def update_todo_valid(self):
        pass

    def update_todo_with_fields_that_not_present_in_todo_model(self):
        pass
