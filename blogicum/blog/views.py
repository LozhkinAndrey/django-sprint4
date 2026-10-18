from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.timezone import now
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import CommentAddForm, PostCreateForm, UserForm
from .models import Category, Comment, Post, User


class OnlySelfMixin(UserPassesTestMixin):
    """Миксин проверки собственника профиля."""

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        obj = self.get_object()
        return obj.id == self.request.user.id


class OnlyAuthorMixin(UserPassesTestMixin):
    """Миксин проверка автора публикации."""

    def test_func(self):
        obj = self.get_object()
        return obj is not None and obj.author_id == self.request.user.id

    def handle_no_permission(self):
        obj = self.get_object()
        if obj:
            return redirect('blog:post_detail', post_id=obj.id)
        return redirect('blog:index')


class OnlyCommentAuthorMixin(UserPassesTestMixin):
    """Миксин проверки автора комментария."""

    def test_func(self):
        obj = self.get_object()
        return obj is not None and obj.author == self.request.user

    def handle_no_permission(self):
        obj = self.get_object()
        if obj:
            return redirect('blog:post_detail', post_id=obj.post_id)
        return redirect('blog:index')


def filtered_select_posts(posts, for_detail_view=False):
    """Фильтр публикаций."""
    qs = posts.select_related('author', 'category', 'location')

    if not for_detail_view:
        qs = qs.filter(
            is_published=True,
            pub_date__lte=now(),
            category__is_published=True,
        )

    return qs.annotate(comments_count=Count('comments')).order_by('-pub_date')


def filtered_select_comments(comments):
    """Фильтр комментариев."""
    return comments.select_related('post', 'author').order_by('created_at')


class PostListView(ListView):
    """Конструктор списка публикаций."""

    model = Post
    queryset = Post.objects.filter(
        pub_date__lte=now(),
        is_published=True,
        category__is_published=True,
    ).annotate(comments_count=Count('comments'))
    ordering = '-pub_date'
    paginate_by = 10
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

    comments = filtered_select_comments(
        Comment.objects,
    ).filter(post_id=post_id)
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
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    post_list = paginator.get_page(page_number)
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
    paginator = Paginator(page_objs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
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

    def get_object(self, queryset=None):
        id = self.kwargs['post_id']
        return get_object_or_404(Post, id=id)

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

    def get_object(self, queryset=None):
        id = self.kwargs['comment_id']
        return get_object_or_404(Comment, id=id)

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

    def get_object(self, queryset=None):
        id = self.kwargs['comment_id']
        return get_object_or_404(Comment, id=id)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.object.post_id},
        )
