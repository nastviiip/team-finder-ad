from django.contrib import admin  # type: ignore[import]

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'status', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('status', 'created_at')

    # Удобное поле для добавления/удаления участников проекта
    filter_horizontal = ('participants',)
