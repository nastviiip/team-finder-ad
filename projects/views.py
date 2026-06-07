# projects/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Project
from .forms import ProjectForm


def project_list(request):
    """Главная страница: список всех проектов от новых к старым"""
    # Получаем все проекты, сортируем по дате создания (минус означает по убыванию)
    project_list = Project.objects.all().order_by("-created_at")

    # Настраиваем пагинацию (по 12 проектов на страницу)
    paginator = Paginator(project_list, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # В шаблон передаем page_obj, но обычно фронтенд ждет переменную 'projects'
    return render(request, "projects/project_list.html", {"projects": page_obj})


def project_details(request, project_id):
    """Детальная страница проекта"""
    project = get_object_or_404(Project, id=project_id)
    return render(request, "projects/project-details.html", {"project": project})


# Продолжаем в projects/views.py


@login_required
def create_project(request):
    """Создание нового проекта"""
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            # commit=False означает "создай объект, но пока не сохраняй в БД"
            project = form.save(commit=False)

            # Автором проекта становится текущий пользователь
            project.owner = request.user
            project.save()  # Теперь сохраняем в БД

            # По заданию: автор автоматически становится участником
            project.participants.add(request.user)

            return redirect("project_details", project_id=project.id)
    else:
        form = ProjectForm()

    return render(
        request,
        "projects/create-project.html",
        {
            "form": form,
            "is_edit": False,  # Флаг для шаблона
        },
    )


@login_required
def edit_project(request, project_id):
    """Редактирование существующего проекта"""
    project = get_object_or_404(Project, id=project_id)

    # Проверка безопасности: только автор может редактировать
    if project.owner != request.user:
        return redirect("project_details", project_id=project.id)

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("project_details", project_id=project.id)
    else:
        form = ProjectForm(instance=project)

    return render(
        request,
        "projects/create-project.html",
        {
            "form": form,
            "is_edit": True,  # Флаг для шаблона
        },
    )


# Продолжаем в projects/views.py


@login_required
def complete_project(request, project_id):
    """Завершение проекта автором (смена статуса на closed)"""
    # Запрос должен быть POST
    if request.method == "POST":
        project = get_object_or_404(Project, id=project_id)

        # Проверяем, что юзер - автор, и проект открыт
        if request.user == project.owner and project.status == "open":
            project.status = "closed"
            project.save()
            # Возвращаем JSON, как требует задание
            return JsonResponse({"status": "ok", "project_status": "closed"})

    return JsonResponse({"error": "Bad request"}, status=400)


@login_required
def toggle_participate(request, project_id):
    """Участвовать / Отказаться от участия"""
    if request.method == "POST":
        project = get_object_or_404(Project, id=project_id)

        if request.user in project.participants.all():
            project.participants.remove(request.user)
        else:
            project.participants.add(request.user)

        # Убрали JsonResponse, добавили нормальный редирект на эту же страницу
        return redirect("project_details", project_id=project.id)
