from django.db import models
from django.conf import settings

from team_finder.constants import (
    PROJECT_NAME_MAX_LEN,
    PROJECT_STATUS_CHOICES,
    PROJECT_STATUS_MAX_LEN,
    STATUS_OPEN,
)


class Project(models.Model):
    name = models.CharField("Название", max_length=PROJECT_NAME_MAX_LEN)
    description = models.TextField("Описание", blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_projects",
        verbose_name="Автор",
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    github_url = models.URLField("Ссылка на GitHub", blank=True, null=True)

    status = models.CharField(
        "Статус",
        max_length=PROJECT_STATUS_MAX_LEN,
        choices=PROJECT_STATUS_CHOICES,
        default=STATUS_OPEN,
    )

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="participated_projects",
        blank=True,
        verbose_name="Участники",
    )

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
