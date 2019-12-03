from graphql_jwt.testcases import JSONWebTokenTestCase
from django.contrib.auth import get_user_model
from model_mommy import mommy
from hamcrest import assert_that, equal_to, has_length
from faker import Faker

from calendars.test_consts import calendars_get, mutation_create
from calendars.models import Calendar
from core.error_messages import EMPTY_CALENDAR_NAME


class Queries(JSONWebTokenTestCase):

    def setUp(self):
        self.default_user = mommy.make(get_user_model())
        self.client.authenticate(self.default_user)

    def test_get_all_calendars_one_calendar(self):
        existed_calendar = mommy.make('calendars.Calendar', user=self.default_user)
        result = self.client.execute(calendars_get).to_dict()

        assert_that(result['data']['calendars'], has_length(1))
        assert_that(result['data']['calendars'][0]['id'], equal_to(str(existed_calendar.id)))

    def test_get_all_calendars_several_calendars(self):
        calendars_to_create = 12
        mommy.make('calendars.Calendar', user=self.default_user, _quantity=calendars_to_create)
        result = self.client.execute(calendars_get).to_dict()

        assert_that(result['data']['calendars'], has_length(calendars_to_create))

    def test_get_all_calendars_for_specific_user(self):
        pass


class Mutations(JSONWebTokenTestCase):

    def setUp(self):
        self.default_user = mommy.make(get_user_model())
        self.client.authenticate(self.default_user)
        self.fake = Faker()

    def test_create_calendar(self):
        new_name = self.fake.word()
        variables = {'name': new_name}
        self.client.execute(mutation_create, variables=variables).to_dict()
        created_calendars = Calendar.objects.filter(name=new_name)
        assert_that(created_calendars, has_length(1))

    def test_create_calendar_with_empty_name(self):
        variables = {'name': ''}
        result = self.client.execute(mutation_create, variables=variables).to_dict()
        assert_that(result['errors'][0]['message'], equal_to(EMPTY_CALENDAR_NAME))
