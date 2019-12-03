from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
import graphene
from graphql.error import GraphQLError

from calendars.models import Calendar
from core.error_messages import EMPTY_CALENDAR_NAME


class CalendarObjectType(DjangoObjectType):

    class Meta:
        model = Calendar


class CalendarQuery(graphene.ObjectType):

    calendars = graphene.List(CalendarObjectType)

    @login_required
    def resolve_calendars(self, info):
        return Calendar.objects.filter(user=info.context.user)


class CreateCalendarMutation(graphene.Mutation):

    class Arguments:
        name = graphene.String(required=True)

    calendar = graphene.Field(CalendarObjectType)

    @login_required
    def mutate(self, info, name):
        if not len(name):
            raise GraphQLError(EMPTY_CALENDAR_NAME)
        new_calendar = Calendar.objects.create(user=info.context.user, name=name)
        return CreateCalendarMutation(calendar=new_calendar)


class CalendarMutation(graphene.ObjectType):
    create_calendar = CreateCalendarMutation.Field()
