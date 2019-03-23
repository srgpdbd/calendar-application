from django.contrib import admin

from todo.models import ToDo
from core.admin import DefaultAdmin


class ToDoAdmin(DefaultAdmin):
    pass


admin.site.register(ToDo, ToDoAdmin)
