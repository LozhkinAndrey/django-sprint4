from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import StaticPageForm
from .models import StaticPage


def csrf_failure(request, reason=''):
    """Конструирует представление для ошибки 403."""
    return render(request, 'pages/403csrf.html', status=403)


def page_not_found(request, exception):
    """Конструирует представление для ошибки 404."""
    return render(request, 'pages/404.html', status=404)


def internal_server_error(request):
    """Конструирует представление для ошибки 500."""
    return render(request, 'pages/500.html', status=500)


class AboutView(TemplateView):
    """Конструирует представление статичной страницы about."""
    template_name = 'pages/about.html'


class RulesView(TemplateView):
    """Конструирует представление статичной страницы rules."""
    template_name = 'pages/rules.html'


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
