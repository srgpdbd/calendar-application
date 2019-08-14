from django.conf import settings
import graphene
from graphene_django.debug import DjangoDebug

from todo.schema import ToDoQuery
from users.schema import UsersQuery, AuthMutation, RegisterObjectsType


class RootQuery(ToDoQuery, UsersQuery, graphene.ObjectType):
    if settings.DEBUG:
        # Debug output - see
        # http://docs.graphene-python.org/projects/django/en/latest/debug/
        debug = graphene.Field(DjangoDebug, name='__debug')


class RootMutation(
    AuthMutation,
    RegisterObjectsType,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=RootQuery, mutation=RootMutation)
