from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    # Авторизация и регистрация
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    # Список пользователей
    path("list/", views.user_list, name="user_list"),
    path(
        "skills/", views.autocomplete_skills, name="autocomplete_skills"
    ),  # GET запрос для автодополнения
    path("<int:user_id>/skills/add/", views.add_skill, name="add_skill"),
    path(
        "<int:user_id>/skills/<int:skill_id>/remove/",
        views.remove_skill,
        name="remove_skill",
    ),
    path('change-password/', views.change_password_view, name='change_password'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    # Профиль пользователя (оставляем в самом низу, чтобы не перехватывал другие url)
    path("<int:user_id>/", views.user_details, name="user_details"),
]
