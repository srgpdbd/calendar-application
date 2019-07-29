from graphene_django import DjangoObjectType
from django_graphene_permissions import permissions_checker
from django_graphene_permissions.permissions import IsAuthenticated
import graphene

from todo.models import ToDo


class ToDoObjectType(DjangoObjectType):

    class Meta:
        model = ToDo


class ToDoQuery(graphene.ObjectType):
    todos = graphene.List(ToDoObjectType)

    @permissions_checker([IsAuthenticated])
    def resolve_todos(self, info):
        return ToDo.objects.all()
