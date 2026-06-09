from . import views

from django.urls import path  # type: ignore[import]

app_name = "projects"

urlpatterns = [
    path("list/", views.project_list, name="project_list"),
    path("create-project/", views.create_project, name="create_project"),
    path("<int:project_id>/", views.project_details, name="project_details"),
    path("<int:project_id>/edit/", views.edit_project, name="edit_project"),
    path("<int:project_id>/complete/", views.complete_project, name="complete_project"),
    path(
        "<int:project_id>/toggle-participate/",
        views.toggle_participate,
        name="toggle_participate",
    ),
]
