from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from graphql.error import GraphQLError
import graphene
import graphql_jwt

from calendars.models import Calendar
from calendars.consts import DEFAULT_CALENDAR_NAME


class AuthMutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()


class UserObjectType(DjangoObjectType):
    class Meta:
        model = User


class UsersQuery(graphene.ObjectType):
    users = graphene.List(UserObjectType)

    def resolve_users(self, info):
        return User.objects.all()


class RegisterMutation(graphene.Mutation):

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password1 = graphene.String(required=True)
        password2 = graphene.String(required=True)

    success = graphene.String()

    def mutate(self, info, username, email, password1, password2):
        if password1 == password2:
            if User.objects.filter(email=email).exists():
                raise GraphQLError(message='User with this email already exists')
            if User.objects.filter(username=username).exists():
                raise GraphQLError(message='User with this username already exists')
            user = User.objects.create(email=email, username=username)
            user.set_password(password1)
            user.save()
            Calendar.objects.create(user=user, name=DEFAULT_CALENDAR_NAME)
            return RegisterMutation(success=True)
        else:
            raise GraphQLError(message='Passwords do not match')


class RegisterObjectsType(graphene.ObjectType):
    register = RegisterMutation().Field()
