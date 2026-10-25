from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.timezone import now
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from core.constants import PAGE_COUNT
from .forms import CommentAddForm, PostCreateForm, UserForm
from .mixins import OnlyAuthorMixin, OnlyCommentAuthorMixin, OnlySelfMixin
from .models import Category, Comment, Post, User
from .service import filtered_select_posts, get_paginate_objects


class PostListView(ListView):
    """Конструктор списка публикаций."""

    model = Post
    queryset = Post.objects.filter(
        pub_date__lte=now(),
        is_published=True,
        category__is_published=True,
    ).annotate(comments_count=Count('comments'))
    ordering = '-pub_date'
    paginate_by = PAGE_COUNT
    template_name = 'blog/index.html'


def post_detail(request, post_id):
    """Конструирует представление деталей публикации."""
    post = get_object_or_404(
        filtered_select_posts(Post.objects, for_detail_view=True),
        id=post_id
    )

    if (not post.is_published) or (not post.category.is_published):
        if post.author != request.user:
            return HttpResponseNotFound()

    comments = post.comments.all().order_by('created_at')
    form = CommentAddForm()

    return render(
        request,
        'blog/detail.html',
        {
            'post': post,
            'comments': comments,
            'user': request.user,
            'form': form,
        },
    )


def category_posts(request, category_slug):
    """Конструирует список публикаций в категории."""
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True,
    )
    posts = filtered_select_posts(category.posts)
    page_number = request.GET.get('page')
    post_list = get_paginate_objects(posts, page_number)
    return render(request, 'blog/category.html', {
        'post_list': post_list,
        'category': category,
        'page_obj': post_list,
    })


def profile(request, username):
    """Конструирует список публикаций пользователя."""
    profile = get_object_or_404(User, username=username)
    page_objs = Post.objects.filter(
        author=profile.id,
    ).annotate(
        comments_count=Count('comments'),
    ).order_by('-pub_date')
    page_number = request.GET.get('page')
    page_obj = get_paginate_objects(page_objs, page_number)
    context = {'profile': profile, 'page_obj': page_obj}
    return render(request, 'blog/profile.html', context)


class UserUpdateView(OnlySelfMixin, UpdateView):
    """Конструктор обновления профиля пользователя."""

    model = User
    form_class = UserForm
    template_name = 'blog/user.html'
    success_url = reverse_lazy('blog:index')

    def get_object(self, queryset=None):
        return self.request.user


class PostCreateView(LoginRequiredMixin, CreateView):
    """Конструктор создания публикации."""

    model = Post
    form_class = PostCreateForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username},
        )


class PostUpdateView(OnlyAuthorMixin, UpdateView):
    """Конструктор редактирования публикации."""

    model = Post
    form_class = PostCreateForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.object.id},
        )


@login_required
def add_comment(request, post_id):
    """Конструирует представление формы добавления комментария к публикации."""
    post = get_object_or_404(Post, id=post_id)
    form = CommentAddForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()

    return redirect('blog:post_detail', post_id=post_id)


class CommentEditView(OnlyCommentAuthorMixin, UpdateView):
    """Конструктор редактирования комментария к публикации."""

    model = Comment
    form_class = CommentAddForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.object.post_id},
        )


class PostDeleteView(OnlyAuthorMixin, DeleteView):
    """Конструктор удаления публикации."""

    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')
    pk_url_kwarg = 'post_id'


class CommentDeleteView(OnlyCommentAuthorMixin, DeleteView):
    """Конструктор удаления комментария."""

    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.object.post_id},
        )
