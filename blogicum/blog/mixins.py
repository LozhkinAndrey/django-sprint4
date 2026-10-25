from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class OnlySelfMixin(UserPassesTestMixin):
    """Миксин проверки собственника профиля."""

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        obj = self.get_object()
        return obj.id == self.request.user.id


class OnlyAuthorMixin(UserPassesTestMixin):
    """Миксин проверки автора публикации."""

    def test_func(self):
        obj = self.get_object()
        return obj.author_id == self.request.user.id

    def handle_no_permission(self):
        obj = self.get_object()
        return redirect('blog:post_detail', post_id=obj.id)


class OnlyCommentAuthorMixin(UserPassesTestMixin):
    """Миксин проверки автора комментария."""

    def test_func(self):
        obj = self.get_object()
        return obj is not None and obj.author == self.request.user

    def handle_no_permission(self):
        obj = self.get_object()
        return redirect('blog:post_detail', post_id=obj.post_id)
