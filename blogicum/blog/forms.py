from django import forms

from .models import Comment, Post, User


class UserForm(forms.ModelForm):
    """Форма пользователя."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def clean(self):
        super().clean()


class PostCreateForm(forms.ModelForm):
    """Форма создания публикации."""

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%d %H:%M',
            ),
            'location': forms.Select(),
            'category': forms.Select(),
        }

    def clean(self):
        return super().clean()


class CommentAddForm(forms.ModelForm):
    """Порма добавления комментария."""

    class Meta:
        model = Comment
        fields = ('text',)
