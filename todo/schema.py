from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
import graphene

from todo.models import ToDo
from calendars.models import Calendar
from labels.schema import LabelType
from labels.models import Label


class ToDoObjectType(DjangoObjectType):

    label = graphene.Field(LabelType)

    @staticmethod
    def resolve_label(todo, info):
        return todo.label

    class Meta:
        model = ToDo


class ToDoQuery(graphene.ObjectType):

    todos = graphene.List(ToDoObjectType, calendar_id=graphene.Int())

    @login_required
    def resolve_todos(self, info, calendar_id):
        return ToDo.objects.filter(calendar__id=calendar_id, calendar__user=info.context.user)


class CreateToDoMutation(graphene.Mutation):

    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String()
        date = graphene.DateTime()
        label_id = graphene.Int()
        calendar_id = graphene.Int(required=True)

    todo = graphene.Field(ToDoObjectType)

    @staticmethod
    @login_required
    def mutate(todo, info, title, calendar_id, description=None, date=None, label_id=None):
        label = Label.objects.get(id=label_id)
        calendar = Calendar.objects.get(id=calendar_id, user=info.context.user)
        new_todo = ToDo.objects.create(
            calendar=calendar,
            title=title,
            description=description,
            date=date,
            label=label,
            # description=description,
            # label_id=label_id,
        )
        return CreateToDoMutation(todo=new_todo)


class ToDoMutation(graphene.ObjectType):
    create_todo = CreateToDoMutation.Field()
