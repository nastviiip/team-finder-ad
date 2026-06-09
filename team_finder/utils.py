from urllib.parse import urlparse
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator

from .constants import PAGE_SIZE


def validate_github_url(value):
    """Строгая проверка, что ссылка ведет именно на домен github.com"""
    if not value:
        return value

    parsed_url = urlparse(value)
    domain = parsed_url.netloc

    if domain not in ("github.com", "www.github.com"):
        raise ValidationError("Ссылка должна вести строго на github.com")
    return value


def get_paginated_page(request, queryset, page_size=PAGE_SIZE):
    """
    Единая функция для пагинации на всём сайте.
    page_size берется из констант по умолчанию, но его можно переопределить.
    """
    paginator = Paginator(queryset, page_size)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)
