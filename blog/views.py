from django.views.generic import ListView, DetailView, CreateView

from .models import Post, Comment


class PostListView(ListView):
    model = Post


class PostDetailView(DetailView):
    model = Post


class CommentListView(ListView):
    model = Comment


class CommentCreateView(CreateView):
    http_method_names = ['post']
    model = Comment
    fields = ('name', 'email', 'text')

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
