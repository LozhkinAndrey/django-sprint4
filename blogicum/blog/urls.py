from django.urls import path, include

from .views import (
    CommentDeleteView,
    CommentEditView,
    UserUpdateView,
    PostCreateView,
    PostDeleteView,
    PostListView,
    PostUpdateView,
    # index,
    add_comment,
    post_detail,
    category_posts,
    profile,
)


app_name = 'blog'


urlpatterns = [
    path('posts/<int:post_id>/', post_detail, name='post_detail'),
    path('category/<slug:category_slug>/', category_posts,
         name='category_posts'),
    path('', PostListView.as_view(), name='index'),
    path('profile/<slug:username>', profile, name='profile'),
    path('edit/', UserUpdateView.as_view(), name='edit_profile'),
    path('posts/create/', PostCreateView.as_view(), name='post_create'),
    path(
        'posts/<int:post_id>/edit/',
        PostUpdateView.as_view(),
        name='post_edit',
    ),
    path(
        'posts/<int:post_id>/comment/',
        add_comment,
        name='add_comment',
    ),
    path(
        'posts/<int:post_id>/edit_comment/<int:comment_id>/',
        CommentEditView.as_view(),
        name='edit_comment',
    ),
    path(
        'posts/<int:post_id>/delete/',
        PostDeleteView.as_view(),
        name='post_delete',
    ),
    path(
        'posts/<int:post_id>/delete_comment/<int:comment_id>/',
        CommentDeleteView.as_view(),
        name='delete_comment',
    ),
]
