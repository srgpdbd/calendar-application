from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from todo.models import ToDo
from todo.serialiers import ToDoSerializer


class ToDoView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = ToDo.active.all()
    serializer_class = ToDoSerializer
