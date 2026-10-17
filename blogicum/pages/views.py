from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import StaticPageForm
from .models import StaticPage


def about(request):
    return render(request, 'pages/about.html')


def rules(request):
    return render(request, 'pages/rules.html')


class StaticPageView(DetailView):
    model = StaticPage
    template_name = 'pages/static_page.html'
    context_object_name = 'page'

    def get_queryset(self):
        return StaticPage.objects.filter(is_published=True)


class AdminOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class StaticPageListView(AdminOnlyMixin, ListView):
    model = StaticPage
    template_name = 'pages/cms/list.html'
    context_object_name = 'pages'
    paginate_by = 20


class StaticPageCreateView(AdminOnlyMixin, CreateView):
    model = StaticPage
    form_class = StaticPageForm
    template_name = 'pages/cms/form.html'
    success_url = '/cms/pages/'


class StaticPageUpdateView(AdminOnlyMixin, UpdateView):
    model = StaticPage
    form_class = StaticPageForm
    template_name = 'pages/cms/form.html'
    success_url = '/cms/pages/'
