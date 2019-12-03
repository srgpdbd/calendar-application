from datetime import datetime
from model_mommy import mommy
from hamcrest import assert_that, equal_to, has_length, has_key
from faker import Faker
from django.contrib.auth import get_user_model
from django.utils import timezone
from graphql_jwt.testcases import JSONWebTokenTestCase

from todo.models import ToDo
from calendar_application.schema import schema
from todo.test_consts import create_mutation, update_mutation
from labels.models import Label
from core.error_messages import LABEL_DOES_NOT_EXISTS


class Queries(JSONWebTokenTestCase):

    def setUp(self):
        self.default_user = mommy.make(get_user_model())
        self.client.authenticate(self.default_user)
        self.calendar = mommy.make('calendars.Calendar', id=1, user=self.default_user)
        # TODO: think I can delete f string vakues and provide them in VARIABLES
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
        # TODO: move all mutations and queries to separate vars
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

    def setUp(self):
        self.default_user = mommy.make(get_user_model())
        self.calendar = mommy.make('calendars.Calendar', id=1, user=self.default_user)
        self.client.authenticate(self.default_user)
        self.fake = Faker()

    def test_create_todo_without_not_mandatory_params(self):
        new_title = self.fake.word()
        variables = {'calendarId': self.calendar.id, 'title': new_title}
        self.client.execute(create_mutation, variables=variables).to_dict()
        created_todo = ToDo.objects.filter(title=new_title)

        assert_that(created_todo, has_length(1))
        assert_that(created_todo[0].calendar_id, equal_to(self.calendar.id))

    def test_create_todo_with_not_mandatory_params(self):
        new_title = self.fake.word()
        description = self.fake.word()
        date_string = "1990-01-01"
        date_for_todo = timezone.make_aware(datetime.strptime(date_string, "%Y-%m-%d"))
        label = Label.objects.all()[0]
        variables = {
            'calendarId': self.calendar.id,
            'title': new_title,
            'description': description,
            'date': date_for_todo,
            'labelId': label.id,
        }
        self.client.execute(create_mutation, variables=variables).to_dict()
        created_todo = ToDo.objects.filter(title=new_title, description=description, date=date_for_todo)

        assert_that(created_todo, has_length(1))
        assert_that(created_todo[0].calendar_id, equal_to(self.calendar.id))
        assert_that(created_todo[0].label, equal_to(label))

    def test_create_todo_with_label_id_not_from_base(self):
        new_title = self.fake.word()
        variables = {'calendarId': self.calendar.id, 'title': new_title, 'labelId': 9000}
        result = self.client.execute(create_mutation, variables=variables).to_dict()

        assert_that(dict(result), has_key('errors'))
        assert_that(result['errors'][0]['message'], equal_to(LABEL_DOES_NOT_EXISTS))

    def test_create_todo_with_fields_that_not_present_in_todo_model(self):
        # TODO: doc for every test
        new_title = self.fake.word()
        variables = {'calendarId': self.calendar.id, 'title': new_title, 'some_test_field': 9000}
        self.client.execute(create_mutation, variables=variables)
        created_todo = ToDo.objects.filter(title=new_title)

        assert_that(created_todo, has_length(1))
        assert_that(created_todo[0].calendar_id, equal_to(self.calendar.id))

    def test_update_todo_valid(self):
        id_to_create = 9000
        label = mommy.make('labels.Label')
        date_string = "1990-01-01"
        date_for_todo = timezone.make_aware(datetime.strptime(date_string, "%Y-%m-%d"))
        mommy.make(
            'todo.ToDo',
            id=id_to_create,
            title=self.fake.word(),
            label=label,
            description=self.fake.word(),
            date=date_for_todo,
            calendar=self.calendar,
            done=False,
        )
        new_title = self.fake.word()
        new_description = self.fake.word()
        new_label = mommy.make('labels.Label')
        new_date = timezone.now()
        variables = {
            'todoId': id_to_create,
            'title': new_title,
            'labelId': new_label.id,
            'date': new_date,
            'description': new_description,
            'done': True,
        }
        self.client.execute(update_mutation, variables=variables)
        updated = ToDo.objects.get(id=id_to_create)

        assert_that(updated.title, equal_to(new_title))
        assert_that(updated.label, equal_to(new_label))
        assert_that(updated.date, equal_to(new_date))
        assert_that(updated.description, equal_to(new_description))
        assert_that(updated.done, equal_to(True))
