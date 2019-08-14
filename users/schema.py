from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import graphene
import graphql_jwt


class AuthMutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


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
            user = User.objects.create(email=email, username=username)
            user.set_password(password1)
            return RegisterMutation(success=True)
        else:
            raise ValidationError('Passwords do not match')


class RegisterObjectsType(graphene.ObjectType):
    register = RegisterMutation().Field()
