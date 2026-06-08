from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from http import HTTPStatus
import json

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .forms import UserProfileEditForm
from .models import User, Skill
from .forms import UserRegistrationForm


def register_view(request):
    form = UserRegistrationForm(request.POST or None)

    if request.method == "GET" or not form.is_valid():
        return render(request, "users/register.html", {"form": form})

    user = form.save()
    login(request, user)
    return redirect("project_list")


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "GET" or not form.is_valid():
        return render(request, "users/login.html", {"form": form})

    user = form.get_user()
    login(request, user)
    return redirect("project_list")


def logout_view(request):
    logout(request)
    return redirect("project_list")


@login_required
def edit_profile(request):
    form = UserProfileEditForm(
        request.POST or None, request.FILES or None, instance=request.user
    )

    if request.method == "GET" or not form.is_valid():
        return render(request, "users/edit_profile.html", {"form": form})

    form.save()
    return redirect("users:user_details", user_id=request.user.id)


def user_list(request):
    users = User.objects.all().order_by("id")

    skill_filter = request.GET.get("skill")

    if skill_filter:
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


def autocomplete_skills(request):
    """Возвращает список навыков при вводе текста"""
    q = request.GET.get("q", "")
    skills = Skill.objects.filter(name__istartswith=q).order_by("name")[:10]

    data = [{"id": skill.id, "name": skill.name} for skill in skills]
    return JsonResponse(data, safe=False)


@login_required
def add_skill(request, user_id):
    """Добавление навыка пользователю"""
    if request.user.id != user_id:
        return JsonResponse({"error": "Доступ запрещен"}, status=403)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            skill_id = data.get("skill_id")
            name = data.get("name")
        except json.JSONDecodeError:
            skill_id = request.POST.get("skill_id")
            name = request.POST.get("name")

        created = False
        added = False
        skill = None

        if skill_id:
            skill = get_object_or_404(Skill, id=skill_id)
        elif name:
            skill, created = Skill.objects.get_or_create(name=name)

        if skill:
            if not request.user.skills.filter(id=skill.id).exists():
                request.user.skills.add(skill)
                added = True

            return JsonResponse(
                {"skill_id": skill.id, "created": created, "added": added}
            )

    return JsonResponse({"error": "Неверный запрос"}, status=400)


@login_required
@require_POST  # noqa: F821
def remove_skill(request, user_id, skill_id):
    """Удаление навыка у пользователя"""
    if request.user.id != user_id:
        return JsonResponse(
            {"error": "Вы не можете удалять навыки других пользователей"},
            status=HTTPStatus.FORBIDDEN,
        )

    if request.method == "POST":
        skill = get_object_or_404(Skill, id=skill_id)
        if request.user.skills.filter(id=skill.id).exists():
            request.user.skills.remove(skill)
            return JsonResponse({"status": "ok"})

    return JsonResponse({"error": "Неверный запрос"}, status=HTTPStatus.BAD_REQUEST)


@login_required
def change_password_view(request):
    form = PasswordChangeForm(user=request.user, data=request.POST or None)

    if request.method == "GET" or not form.is_valid():
        return render(request, "users/change_password.html", {"form": form})

    form.save()
    update_session_auth_hash(request, form.user)
    return redirect("users:user_details", user_id=request.user.id)
