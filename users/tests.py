from django.test import TestCase
from django.contrib.auth.models import User
from faker import Faker
from hamcrest import assert_that, has_length, raises, calling
from graphql.error import GraphQLError
from model_mommy import mommy

from users.schema import RegisterMutation, UsersQuery


class Queries(TestCase):

    def test_get_all_users_without_users(self):
        assert_that(UsersQuery().resolve_users(info=None), has_length(0))

    def test_get_all_users_one_user(self):
        mommy.make(User)
        assert_that(UsersQuery().resolve_users(info=None), has_length(1))

    def test_get_all_users_more_than_one(self):
        users_to_create = 12
        mommy.make(User, _quantity=users_to_create)
        assert_that(UsersQuery().resolve_users(info=None), has_length(users_to_create))


class Mutations(TestCase):

    def setUp(self):
        self.fake = Faker()
        self.mutation = RegisterMutation().mutate

    def test_create_new_user(self):
        email = self.fake.email()
        username = self.fake.word()
        password = self.fake.password()
        self.mutation(
            info=None,
            username=username,
            email=email,
            password1=password,
            password2=password,
        )
        users = User.objects.filter(username=username, email=email)
        assert_that(users, has_length(1))

    def test_create_new_user_with_pass_missmatch(self):
        email = self.fake.email()
        username = self.fake.word()
        first_pass = 'testpass'
        second_pass = 'testpass2'
        assert_that(
            calling(self.mutation).with_args(
                email=email, username=username, password1=first_pass, password2=second_pass, info=None
            ),
            raises(GraphQLError)
        )

    def test_create_user_with_existed_username(self):
        email = self.fake.email()
        password = self.fake.password()
        existed_user = mommy.make(User)
        assert_that(
            calling(self.mutation).with_args(
                email=email, username=existed_user.username, password1=password, password2=password, info=None
            ),
            raises(GraphQLError)
        )

    def test_create_user_with_existed_email(self):
        username = self.fake.word()
        password = self.fake.password()
        existed_user = mommy.make(User)
        assert_that(
            calling(self.mutation).with_args(
                email=existed_user.email, username=username, password1=password, password2=password, info=None
            ),
            raises(GraphQLError)
        )
