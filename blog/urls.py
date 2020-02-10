from django.urls import path,include
from django.conf.urls import url

from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView

urlpatterns = [
    path('<slug:slug>', PostDetailView.as_view(), name='post_detail'),
    path('', PostListView.as_view(), name='post_list'),
    path('add/', PostCreateView.as_view(), name='post_add'),
    path('update/<slug:slug>', PostUpdateView.as_view(), name='post_update'),
    url(r'comments/', include('django_comments.urls')),
]
