from django.urls import path

from .views import PostListView, PostDetailView, CommentCreateView

urlpatterns = [
    path('<slug:slug>', PostDetailView.as_view(), name='post_detail'),
    path('', PostListView.as_view(), name='post_list'),
    path('<slug:slug>/add_comment', CommentCreateView.as_view(), name='create_comment')
]
