from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import Post


class PostListView(ListView):
    model = Post


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    fields = '__all__'
    permission_required = "auth.change_user"
    success_url = reverse_lazy('post_list')
    login_url = 'home'

    def get_login_url(self):
        """
        Override this method to override the login_url attribute.
        """
        login_url = self.login_url
        if not login_url:
            raise NotImplementedError(
                '{0} is missing the login_url attribute. Define {0}.login_url, settings.LOGIN_URL, or override '
                '{0}.get_login_url().'.format(self.__class__.__name__)
            )
        return str(login_url)


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    fields = '__all__'
    permission_required = "auth.change_user"
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'slug': self.kwargs['slug']})