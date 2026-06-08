from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from team_finder.constants import USER_NAME_MAX_LEN, PHONE_MAX_LEN, ABOUT_MAX_LEN


class Skill(models.Model):
    name = models.CharField("Название", max_length=124, unique=True)

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"
        ordering = ["name"]

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField("Имя", max_length=USER_NAME_MAX_LEN)
    surname = models.CharField("Фамилия", max_length=USER_NAME_MAX_LEN)
    avatar = models.ImageField(upload_to="avatars/")
    phone = models.CharField("Телефон", max_length=PHONE_MAX_LEN, unique=True)
    github_url = models.URLField("Ссылка на GitHub", blank=True, null=True)
    about = models.TextField("О себе", max_length=ABOUT_MAX_LEN, blank=True, null=True)
    is_active = models.BooleanField("Активен", default=True)
    is_staff = models.BooleanField("Персонал", default=False)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["id"]

    skills = models.ManyToManyField(Skill, related_name="users", blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname", "phone"]

    def __str__(self):
        return f"{self.name} {self.surname}"
