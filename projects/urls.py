from django.urls import path
from . import views  # Импортируем вьюхи из текущего приложения

urlpatterns = [
    # Список проектов
    path("list/", views.project_list, name="project_list"),
    # Создание проекта
    path("create-project/", views.create_project, name="create_project"),
    # Детальная страница проекта (id - это число)
    path("<int:project_id>/", views.project_details, name="project_details"),
    # Редактирование проекта
    path("<int:project_id>/edit/", views.edit_project, name="edit_project"),
    # Завершить проект (POST запрос)
    path("<int:project_id>/complete/", views.complete_project, name="complete_project"),
    # Участвовать / Отказаться (POST запрос)
    path(
        "<int:project_id>/toggle-participate/",
        views.toggle_participate,
        name="toggle_participate",
    ),
]
