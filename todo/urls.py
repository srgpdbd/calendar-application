from django.urls import path
from todo.views import ToDoView


urlpatterns = [
    path('', ToDoView.as_view(), name='todos'),
]
