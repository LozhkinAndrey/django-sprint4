from django.db import models


# Модель можно вынести в приложение Core либо оставить в приложении Blog.
class PublishedAndCreatedAt(models.Model):
    """Модель отслеживания даты публикации и разрешения на публикацию."""

    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('created_at', )
