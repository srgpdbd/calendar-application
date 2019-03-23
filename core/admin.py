from django.contrib import admin


class DefaultAdmin(admin.ModelAdmin):

    default_readonly_fields = ('deleted_at',)

    def get_readonly_fields(self, request, obj=None):
        for field in self.default_readonly_fields:
            if (hasattr(obj, field)) and not field in self.readonly_fields:
                self.readonly_fields += (field,)
        return self.readonly_fields
