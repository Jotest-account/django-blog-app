from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from users.models import CustomUser

from .models import Post, PostViews


class PostListView(ListView):
    model = Post


class PostDetailView(DetailView):
    model = Post

    def get_object(self):
        obj = super().get_object()
        obj.num_views = obj.num_views + 1 if obj.num_views else 1
        obj.save()

        user = self.request.user
        if user.is_anonymous:
            user = get_user_model().objects.get(username='anonymous')

        try:
            user_post_views = PostViews.objects.get(user=user, post=obj)
        except PostViews.DoesNotExist:
            user_post_views = None

        if not user_post_views:
            PostViews.objects.create(user=user, post_id=obj.id, post_views=1)
        else:
            post_views = PostViews.objects.get(id=user_post_views.id)
            post_views.post_views += 1
            post_views.save()

        return obj


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