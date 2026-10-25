from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.db import models
from django.utils.html import format_html

from .models import Category, Location, Post, User

admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Админ-панель для пользователей."""

    list_display = ('id', 'username', 'email', 'first_name',
                    'last_name', 'posts_count')
    search_fields = ('username', 'email')
    list_filter = ('username', 'email')
    list_display_links = ('username', 'id')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Личная информация', {'fields': ('first_name', 'last_name')})
    )

    @admin.display(description='Постов у пользователя')
    def posts_count(self, obj):
        return obj.posts.count()


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Админ-панель для управления публикациями."""

    image = models.ImageField(upload_to='post_images')
    search_fields = ('text', )
    list_display = ('id', 'title', 'category', 'location', 'text', 'image_tag',
                    'author', 'created_at', 'pub_date', 'is_published')
    list_display_links = ('title', )
    list_editable = ('category', 'is_published', 'location')
    list_filter = ('created_at', )
    empty_value_display = '-пусто-'
    readonly_fields = ('image_tag', )

    def image_tag(self, post):
        if post.image:
            return format_html(
                '<img src="{}" width="200" height="200" />',
                post.image.url,
            )

    image_tag.short_description = 'Изображение'

    fieldsets = (
        (None, {
            'fields': ('title',
                       ('category', 'location'),
                       ('text', 'image_tag'),
                       'author',
                       ('pub_date', 'is_published'))
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админ-панель для категорий."""

    search_fields = ('title', )
    list_display = ('pk', 'title', 'description', 'slug',
                    'is_published', 'created_at')
    list_editable = ('slug', 'is_published')
    list_filter = ('created_at', )
    empty_value_display = '-пусто-'


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Админ-панель для локаций."""

    search_fields = ('name', )
    list_display = ('pk', 'name', 'is_published', 'created_at')
    list_editable = ('is_published', )
    list_filter = ('created_at', )
    empty_value_display = '-пусто-'


admin.site.unregister(Group)
