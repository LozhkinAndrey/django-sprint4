from django.db import models


class StaticPage(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    slug = models.SlugField(
        "URL-идентификатор",
        unique=True,
        help_text="Только латиница, цифры, дефисы.",
    )
    content = models.TextField(
        "Контент (HTML)",
        blank=True,
        help_text="Можно использовать HTML-теги",
    )
    is_published = models.BooleanField("Опубликовано", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Статичная страница"
        verbose_name_plural = "Статичные страницы"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/{self.slug}/"
