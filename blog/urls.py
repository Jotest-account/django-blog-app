from django.urls import path,include
from django.conf.urls import url

from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path('<slug:slug>', PostDetailView.as_view(), name='post_detail'),
    path('', PostListView.as_view(), name='post_list'),
    path('add/', PostCreateView.as_view(), name='post_add'),
    path('<slug:slug>/upate', PostUpdateView.as_view(), name='post_update'),
    path('<slug:slug>/delete', PostDeleteView.as_view(), name='post_delete'),
    url(r'comments/', include('django_comments.urls')),
]
