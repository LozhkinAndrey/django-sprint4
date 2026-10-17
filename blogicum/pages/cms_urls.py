from django.urls import path

from .views import (StaticPageCreateView, StaticPageListView,
                    StaticPageUpdateView, StaticPageView)

app_name = 'cms'


urlpatterns = [
    path('pages/', StaticPageListView.as_view(), name='cms_page_list'),
    path('<slug:slug>/', StaticPageView.as_view(), name='cms_static_page'),
    path(
        'pages/create/',
        StaticPageCreateView.as_view(),
        name='cms_page_create',
    ),
    path(
        'pages/<int:pk>/edit/',
        StaticPageUpdateView.as_view(),
        name='cms_page_edit',
    ),
]
