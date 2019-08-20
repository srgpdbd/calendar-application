from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
import graphene

from todo.models import ToDo


class ToDoObjectType(DjangoObjectType):

    class Meta:
        model = ToDo


class ToDoQuery(graphene.ObjectType):
    todos = graphene.List(ToDoObjectType)

    @login_required
    def resolve_todos(self, info):
        return ToDo.objects.all()
