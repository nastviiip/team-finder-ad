from django.contrib import admin
from .models import User, Skill

# Регистрируем навык
admin.site.register(Skill)

# Регистрируем пользователя (с красивым отображением колонок)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'surname', 'phone', 'is_staff')
    search_fields = ('email', 'name', 'surname', 'phone')
    list_filter = ('is_staff', 'is_active')
    
    # Чтобы навыки отображались удобным полем с выбором
    filter_horizontal = ('skills',)