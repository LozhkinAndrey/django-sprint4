from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import StaticPageForm
from .models import StaticPage


def about(request):
    """Конструирует представление статичной страницы about."""
    return render(request, 'pages/about.html')


def rules(request):
    """Конструирует представление статичной страницы rules."""
    return render(request, 'pages/rules.html')


class StaticPageView(DetailView):
    """Конструктор статичной страницы."""
    model = StaticPage
    template_name = 'pages/static_page.html'
    context_object_name = 'page'

    def get_queryset(self):
        return StaticPage.objects.filter(is_published=True)


class AdminOnlyMixin(UserPassesTestMixin):
    """Миксин проверки на суперпользователя."""
    def test_func(self):
        return self.request.user.is_superuser


class StaticPageListView(AdminOnlyMixin, ListView):
    """Конструктор списка статичных страниц."""
    model = StaticPage
    template_name = 'pages/cms/list.html'
    context_object_name = 'pages'
    paginate_by = 20


class StaticPageCreateView(AdminOnlyMixin, CreateView):
    """Конструктор создания статичной страницы."""
    model = StaticPage
    form_class = StaticPageForm
    template_name = 'pages/cms/form.html'
    success_url = '/cms/pages/'


class StaticPageUpdateView(AdminOnlyMixin, UpdateView):
    """Конструктор обновления статичной страницы."""
    model = StaticPage
    form_class = StaticPageForm
    template_name = 'pages/cms/form.html'
    success_url = '/cms/pages/'
