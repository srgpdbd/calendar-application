import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from labels.models import Label


class LabelType(DjangoObjectType):

    class Meta:
        model = Label


class LabelQuery(graphene.ObjectType):

    labels = graphene.List(LabelType)

    @login_required
    def resolve_labels(self, info):
        # TODO: here will be not all labels, but labels for specific user
        return Label.objects.all()
