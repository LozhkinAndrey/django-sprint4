from django.core.paginator import Paginator
from django.db.models import Count
from django.utils.timezone import now

from core.constants import PAGE_COUNT


def filtered_select_posts(posts, for_detail_view=False):
    """Фильтр публикаций."""
    qs = posts.select_related('author', 'category', 'location')

    if not for_detail_view:
        qs = qs.filter(
            is_published=True,
            pub_date__lte=now(),
            category__is_published=True,
        )

    return qs.annotate(comments_count=Count('comments')).order_by('-pub_date')


def get_paginate_objects(set, page_number):
    """Возвращает нужную страницу из списка объектов."""
    paginator = Paginator(set, PAGE_COUNT)
    return paginator.get_page(page_number)
