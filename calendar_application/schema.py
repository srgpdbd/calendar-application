from django.conf import settings
import graphene
from graphene_django.debug import DjangoDebug

from todo.schema import ToDoQuery, ToDoMutation
from labels.schema import LabelQuery
from calendars.schema import CalendarQuery, CalendarMutation
from users.schema import UsersQuery, AuthMutation, RegisterObjectsType


QUERIES = (
    ToDoQuery,
    CalendarQuery,
    UsersQuery,
    LabelQuery,
)

MUTATIONS = (
    AuthMutation,
    RegisterObjectsType,
    CalendarMutation,
    ToDoMutation,
)


class RootQuery(*QUERIES, graphene.ObjectType):
    if settings.DEBUG:
        # Debug output - see
        # http://docs.graphene-python.org/projects/django/en/latest/debug/
        debug = graphene.Field(DjangoDebug, name='__debug')


class RootMutation(*MUTATIONS, graphene.ObjectType):
    pass


schema = graphene.Schema(query=RootQuery, mutation=RootMutation)
