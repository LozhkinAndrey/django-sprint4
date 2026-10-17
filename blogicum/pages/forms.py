from django import forms

from .models import StaticPage


class StaticPageForm(forms.ModelForm):
    class Meta:
        model = StaticPage
        fields = ['title', 'slug', 'content', 'is_published']
        widgets = {
            'content': forms.Textarea(
                attrs={'rows': 20, 'class': 'form-control'},
            ),
        }
