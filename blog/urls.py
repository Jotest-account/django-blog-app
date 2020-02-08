from django.urls import path,include
from django.conf.urls import url

from .views import PostListView, PostDetailView

urlpatterns = [
    path('<slug:slug>', PostDetailView.as_view(), name='post_detail'),
    path('', PostListView.as_view(), name='post_list'),
    url(r'comments/', include('django_comments.urls')),
]
