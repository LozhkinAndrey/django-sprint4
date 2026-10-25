from django.urls import path, include

from .views import (CommentDeleteView, CommentEditView, PostCreateView,
                    PostDeleteView, PostListView, PostUpdateView,
                    UserUpdateView, add_comment, category_posts, post_detail,
                    profile)

app_name = 'blog'

post_urls = [
    path('<int:post_id>/', post_detail, name='post_detail'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path(
        '<int:post_id>/edit/',
        PostUpdateView.as_view(),
        name='post_edit',
    ),
    path(
        '<int:post_id>/comment/',
        add_comment,
        name='add_comment',
    ),
    path(
        '<int:post_id>/edit_comment/<int:comment_id>/',
        CommentEditView.as_view(),
        name='edit_comment',
    ),
    path(
        '<int:post_id>/delete/',
        PostDeleteView.as_view(),
        name='post_delete',
    ),
    path(
        '<int:post_id>/delete_comment/<int:comment_id>/',
        CommentDeleteView.as_view(),
        name='delete_comment',
    ),
]

urlpatterns = [
    path('category/<slug:category_slug>/', category_posts,
         name='category_posts'),
    path('', PostListView.as_view(), name='index'),
    path('profile/<slug:username>', profile, name='profile'),
    path('edit/', UserUpdateView.as_view(), name='edit_profile'),
    path('posts/', include(post_urls))
]
