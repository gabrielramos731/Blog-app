from django.urls import path
from .views import (
    BlogListView,
    BlogDetailView,
    BlogCreateView,
    BlogUpdateView,
    BlogDeleteView,
    BlogPostSearchListView,
    BlogAuthPostSearchListView,
)

urlpatterns = [
    path('', BlogListView.as_view(), name='home'),
    path('post/<int:pk>', BlogDetailView.as_view(), name='post_detail'),
    path('post/new', BlogCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/edit', BlogUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete', BlogDeleteView.as_view(), name='post_delete'),
    path('busca/', BlogPostSearchListView.as_view(), name='post_search'),
    path('autor/', BlogAuthPostSearchListView.as_view(), name='autor_post_search'),
]
