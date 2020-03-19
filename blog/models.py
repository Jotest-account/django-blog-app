from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django_comments.moderation import CommentModerator, moderator
from django_extensions.db.fields import AutoSlugField
from django_lifecycle import LifecycleModelMixin, hook
from markdownx.utils import markdownify
from martor.models import MartorField


class TimeStampedModel(models.Model):
    added = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(LifecycleModelMixin, TimeStampedModel):
    title = models.CharField(max_length=200)
    body = MartorField(default='')
    slug = AutoSlugField(null=True, default=None, unique=True, populate_from='title')
    content_edited = models.DateTimeField(null=True)
    num_views = models.IntegerField(null=True)

    def __str__(self):
        return f'Post: {self.title}'

    class Meta:
        ordering = ['-added']

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.slug)])

    @property
    def formatted_markdown(self):
        return markdownify(self.body)

    @property
    def body_summary(self):
        if len(self.body) > 300:
            return f'{self.body[:300]}...'
        else:
            return self.body

    @hook('before_update', when_any=['title', 'body'], has_changed=True)
    def on_update(self):
        update_setting = BlogSettings.objects.get(setting_name='modify_title_on_edit')
        if update_setting.setting_value == 'True':
            if not self.title.strip().endswith('(Edited)'):
                self.title = f'{self.title} (Edited)'
            self.content_edited = datetime.now()


class PostViews(models.Model):
    post_views = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, )
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Post views: {self.post} - (by {self.user})'

    class Meta:
        ordering = ['-updated']


class BlogSettings(TimeStampedModel):
    setting_name = models.CharField(max_length=100)
    setting_value = models.CharField(max_length=100)

    def __str__(self):
        return f'Setting: {self.setting_name} = {self.setting_value}'

    class Meta:
        ordering = ['-setting_name']


class PostModerator(CommentModerator):
    email_notification = True


moderator.register(Post, PostModerator)
