from model_mommy import mommy
from hamcrest import assert_that, has_length
from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase

from labels.models import Label
from labels.test_consts import query


class Queries(JSONWebTokenTestCase):

    def setUp(self):
        self.default_user = mommy.make(get_user_model())
        self.client.authenticate(self.default_user)
        self.migrated_labels = Label.objects.all().count()

    def test_get_all_prepopulated(self):
        result = self.client.execute(query).to_dict()
        assert_that(result['data']['labels'], has_length(self.migrated_labels))

    def test_get_all_with_additional(self):
        new_labels = mommy.make('labels.Label', _quantity=12)
        labels_to_be_in_db = self.migrated_labels + len(new_labels)
        result = self.client.execute(query).to_dict()
        assert_that(result['data']['labels'], has_length(labels_to_be_in_db))
