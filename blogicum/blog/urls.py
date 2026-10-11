from django.urls import path, include

from .views import (
    UserUpdateView,
    PostListView,
    # index,
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
]
