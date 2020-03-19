import json
import os
import uuid

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from .models import Post, PostViews, BlogSettings
from .forms import PostForm

import logging

logger = logging.getLogger(__name__)


class PostListView(ListView):
    model = Post
    paginate_by = 2


class PostDetailView(DetailView):
    model = Post

    def get_object(self):
        obj = super().get_object()
        logger.error("###############################")
        logger.error("I am in the PostDetailView")
        logger.error("###############################")

        update_setting = BlogSettings.objects.get(setting_name='register_post_visits')
        if update_setting.setting_value == 'True':
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
    # fields = '__all__'
    fields = ('title', 'body')
    permission_required = "blog.add_post"
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
    # fields = '__all__'
    permission_required = 'blog.change_post'
    template_name_suffix = '_update_form'
    form_class = PostForm

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'slug': self.kwargs['slug']})


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    permission_required = 'blog.delete_post'

    success_url = reverse_lazy('post_list')


from martor.utils import LazyEncoder


@login_required
def markdown_uploader(request):
    """
    Makdown image upload for locale storage
    and represent as json to markdown editor.
    """
    if request.method == 'POST' and request.is_ajax():
        if 'markdown-image-upload' in request.FILES:
            image = request.FILES['markdown-image-upload']
            image_types = [
                'image/png', 'image/jpg',
                'image/jpeg', 'image/pjpeg', 'image/gif'
            ]
            if image.content_type not in image_types:
                data = json.dumps({
                    'status': 405,
                    'error': ('Bad image format.')
                }, cls=LazyEncoder)
                return HttpResponse(
                    data, content_type='application/json', status=405)

            if image.size > settings.MAX_IMAGE_UPLOAD_SIZE:
                to_MB = settings.MAX_IMAGE_UPLOAD_SIZE / (1024 * 1024)
                data = json.dumps({
                    'status': 405,
                    'error': _('Maximum image file is %(size) MB.') % {'size': to_MB}
                }, cls=LazyEncoder)
                return HttpResponse(
                    data, content_type='application/json', status=405)

            img_uuid = "{0}-{1}".format(uuid.uuid4().hex[:10], image.name.replace(' ', '-'))
            tmp_file = os.path.join(settings.MARTOR_UPLOAD_PATH, img_uuid)
            def_path = default_storage.save(tmp_file, ContentFile(image.read()))
            img_url = os.path.join(settings.MEDIA_URL, def_path)

            data = json.dumps({
                'status': 200,
                'link': img_url,
                'name': image.name
            })
            return HttpResponse(data, content_type='application/json')
        return HttpResponse(_('Invalid request!'))
    return HttpResponse(_('Invalid request!'))