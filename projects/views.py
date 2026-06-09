from http import HTTPStatus

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from .models import Project
from .forms import ProjectForm
from team_finder.utils import get_paginated_page
from team_finder.constants import STATUS_CLOSED, STATUS_OPEN


def project_list(request):
    projects = Project.objects.all()
    page_obj = get_paginated_page(request, projects)
    return render(request, "projects/project_list.html", {"projects": page_obj})


@login_required
def create_project(request):
    form = ProjectForm(request.POST or None)

    if not form.is_valid():
        return render(
            request, "projects/create-project.html", {"form": form, "is_edit": False}
        )

    project = form.save(commit=False)
    project.owner = request.user
    project.save()
    project.participants.add(request.user)
    return redirect("project_details", project_id=project.id)


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if project.owner != request.user:
        return redirect("project_details", project_id=project.id)

    form = ProjectForm(request.POST or None, instance=project)

    if not form.is_valid():
        return render(
            request, "projects/create-project.html", {"form": form, "is_edit": True}
        )

    form.save()
    return redirect("project_details", project_id=project.id)


@login_required
@require_POST
def complete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user != project.owner or project.status != STATUS_OPEN:
        return JsonResponse(
            {"error": "Неверный запрос или нет прав"}, status=HTTPStatus.BAD_REQUEST
        )

    project.status = STATUS_CLOSED
    project.save()
    return JsonResponse(
        {"status": "ok", "project_status": project.status}, status=HTTPStatus.OK
    )


@login_required
@require_POST
def toggle_participate(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if project.participants.filter(id=request.user.id).exists():
        project.participants.remove(request.user)
    else:
        project.participants.add(request.user)

    return JsonResponse({"status": "ok"}, status=HTTPStatus.OK)


def project_details(request, project_id):
    """Детальная страница проекта"""
    project = get_object_or_404(Project, id=project_id)
    return render(request, "projects/project-details.html", {"project": project})
