from django.views.generic import ListView, DetailView, CreateView

from .models import Post


class PostListView(ListView):
    model = Post


class PostDetailView(DetailView):
    model = Post
