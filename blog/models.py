import uuid
from datetime import datetime

from django.db import models
from django_extensions.db.fields import AutoSlugField
from django_comments.moderation import CommentModerator, moderator
from django.contrib.auth import get_user_model
from django.urls import reverse

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
        # if self.has_changed('body') or self.has_changed('title'):
        if not self.title.strip().endswith('(Edited)'):
            self.title = f'{self.title} (Edited)'
        self.content_edited = datetime.now()

    # @hook('before_create')
    # def on_create(self):
    #     self.content_edited = datetime.now()


class PostViews(models.Model):
    post_views = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, )
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Post views: {self.post} - (by {self.user})'

    class Meta:
        ordering = ['-updated']


class PostModerator(CommentModerator):
    email_notification = True


moderator.register(Post, PostModerator)
