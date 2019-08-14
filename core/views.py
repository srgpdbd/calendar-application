from graphene_django.views import GraphQLView
from django.core.exceptions import ValidationError


class CustomGraphQLView(GraphQLView):

    def format_error(self, error):
        if hasattr(error, 'original_error') and isinstance(error.original_error, ValidationError):
            return {'non_field_errors': error.message}
        return super(CustomGraphQLView, self).format_error(error)
