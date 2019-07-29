from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
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
