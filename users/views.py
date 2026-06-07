# users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
import json
from .models import User, Skill
from .forms import UserRegistrationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Сразу авторизуем после регистрации
            return redirect("project_list")  # Перекидываем на главную
    else:
        form = UserRegistrationForm()
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("project_list")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("project_list")


# Добавь это в users/views.py
from django.contrib.auth.decorators import login_required
from .forms import UserProfileEditForm


@login_required
def edit_profile(request):  # <--- УБРАЛИ user_id отсюда
    if request.method == "POST":
        form = UserProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("users:user_details", user_id=request.user.id)
    else:
        form = UserProfileEditForm(instance=request.user)

    return render(request, "users/edit_profile.html", {"form": form})


# Добавь это в users/views.py
def user_list(request):
    # Получаем всех пользователей, сортируем по id
    users = User.objects.all().order_by("id")

    # Смотрим, есть ли в URL параметр skill (например, /users/list/?skill=Python)
    skill_filter = request.GET.get("skill")

    if skill_filter:
        # Оставляем только тех юзеров, у которых в навыках есть это название
        users = users.filter(skills__name=skill_filter)

    all_skills = Skill.objects.all()

    context = {
        "participants": users,
        "all_skills": all_skills,
        "active_skill": skill_filter,
    }
    return render(request, "users/participants.html", context)


def user_details(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, "users/user-details.html", {"user": user})


# Добавь это в users/views.py


def autocomplete_skills(request):
    """Возвращает список навыков при вводе текста"""
    q = request.GET.get("q", "")
    # Ищем навыки, которые начинаются на букву/слово `q`, берем первые 10
    skills = Skill.objects.filter(name__istartswith=q).order_by("name")[:10]

    # Формируем список словарей
    data = [{"id": skill.id, "name": skill.name} for skill in skills]
    return JsonResponse(data, safe=False)


@login_required
def add_skill(request, user_id):
    """Добавление навыка пользователю"""
    # Проверка безопасности
    if request.user.id != user_id:
        return JsonResponse({"error": "Доступ запрещен"}, status=403)

    if request.method == "POST":
        # JS часто отправляет данные в формате JSON, прочитаем их
        try:
            data = json.loads(request.body)
            skill_id = data.get("skill_id")
            name = data.get("name")
        except json.JSONDecodeError:
            # Если это обычный POST запрос, а не JSON
            skill_id = request.POST.get("skill_id")
            name = request.POST.get("name")

        created = False
        added = False
        skill = None

        if skill_id:
            # Если передан ID, находим существующий навык
            skill = get_object_or_404(Skill, id=skill_id)
        elif name:
            # Если передано имя, находим навык или создаем новый
            skill, created = Skill.objects.get_or_create(name=name)

        if skill:
            # Проверяем, нет ли уже этого навыка у юзера
            if not request.user.skills.filter(id=skill.id).exists():
                request.user.skills.add(skill)
                added = True

            return JsonResponse(
                {"skill_id": skill.id, "created": created, "added": added}
            )

    return JsonResponse({"error": "Неверный запрос"}, status=400)


@login_required
def remove_skill(request, user_id, skill_id):
    """Удаление навыка у пользователя"""
    if request.user.id != user_id:
        return JsonResponse({"error": "Доступ запрещен"}, status=403)

    if request.method == "POST":
        skill = get_object_or_404(Skill, id=skill_id)
        if request.user.skills.filter(id=skill.id).exists():
            request.user.skills.remove(skill)
            return JsonResponse({"status": "ok"})

    return JsonResponse({"error": "Неверный запрос"}, status=400)


@login_required
def change_password_view(request):
    if request.method == "POST":
        # Передаем текущего юзера и данные из формы
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Эта функция нужна, чтобы пользователя не "выкинуло" из аккаунта после смены пароля
            update_session_auth_hash(request, form.user)
            return redirect("users:user_details", user_id=request.user.id)
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, "users/change_password.html", {"form": form})
