from datetime import datetime, time
from django.utils.timezone import make_aware
from graphene_django import DjangoObjectType
from graphql.error import GraphQLError
from graphql_jwt.decorators import login_required
import graphene

from todo.models import ToDo
from calendars.models import Calendar
from labels.schema import LabelType
from labels.models import Label
from core.error_messages import LABEL_DOES_NOT_EXISTS


class ToDoObjectType(DjangoObjectType):

    label = graphene.Field(LabelType)

    @staticmethod
    def resolve_label(todo, info):
        return todo.label

    class Meta:
        model = ToDo


class ToDoQuery(graphene.ObjectType):

    todos = graphene.List(ToDoObjectType, calendar_id=graphene.Int(), date=graphene.Date(required=False))

    @login_required
    def resolve_todos(self, info, calendar_id, date=None):
        query = {
            'calendar__id': calendar_id,
            'calendar__user': info.context.user,
        }
        if date:
            query['date__range'] = (
                make_aware(datetime.combine(date, time.min)),
                make_aware(datetime.combine(date, time.max))
            )
        return ToDo.objects.filter(**query).order_by('done')


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
        calendar = Calendar.objects.get(id=calendar_id, user=info.context.user)

        try:
            label = Label.objects.get(id=label_id) if label_id else None
        except Label.DoesNotExist:
            raise GraphQLError(LABEL_DOES_NOT_EXISTS)

        new_todo = ToDo.objects.create(
            calendar=calendar,
            title=title,
            description=description,
            date=date,
            label=label,
        )
        return CreateToDoMutation(todo=new_todo)


class UpdateToDoMutation(graphene.Mutation):

    class Arguments:
        todo_id = graphene.Int()
        title = graphene.String()
        description = graphene.String()
        date = graphene.DateTime()
        label_id = graphene.Int()
        done = graphene.Boolean()

    todo = graphene.Field(ToDoObjectType)

    @staticmethod
    @login_required
    def mutate(todo, info, todo_id, **kwargs):
        updated_todo = ToDo.objects.get(id=todo_id)
        for key, value in kwargs.items():
            setattr(updated_todo, key, value)
        updated_todo.save()
        return CreateToDoMutation(todo=updated_todo)


class ToDoMutation(graphene.ObjectType):
    create_todo = CreateToDoMutation.Field()
    update_todo = UpdateToDoMutation.Field()
