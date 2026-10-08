from django.shortcuts import get_object_or_404, render
from django.utils.timezone import now
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import UpdateView

from core.constants import POSTS_BY_PAGE
from .models import Category, Post, User
from .forms import UserForm


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        obj = self.get_object()
        return obj.id == self.request.user.id


def filtered_select_posts(posts):
    return posts.select_related(
        'author', 'category', 'location'
    ).filter(
        is_published=True,
        pub_date__lt=now(),
        category__is_published=True,
    )


def index(request):
    post_list = filtered_select_posts(Post.objects)[:POSTS_BY_PAGE]
    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request, post_id):
    post = get_object_or_404(
        filtered_select_posts(Post.objects),
        id=post_id
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True
    )
    post_list = filtered_select_posts(category.posts)
    return render(request, 'blog/category.html', {
        'post_list': post_list,
        'category': category
    })


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    page_obj = Post.objects.filter(author=profile.id)
    context = {'profile': profile, 'page_obj': page_obj}
    return render(request, 'blog/profile.html', context)


class UserUpdateView(OnlyAuthorMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'blog/user.html'
    success_url = reverse_lazy('blog:index')

    def get_object(self, queryset=None):
        return self.request.user
