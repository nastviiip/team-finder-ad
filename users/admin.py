from django.contrib import admin

from .models import User, Skill

admin.site.register(Skill)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'surname', 'phone', 'is_staff')
    search_fields = ('email', 'name', 'surname', 'phone')
    list_filter = ('is_staff', 'is_active')
    filter_horizontal = ('skills',)
