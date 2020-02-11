import uuid

from django.db import models
from django_extensions.db.fields import AutoSlugField
from django_comments.moderation import CommentModerator, moderator
from django.contrib.auth import get_user_model

from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


class Post(models.Model):
    title = models.CharField(max_length=200)
    body = MarkdownxField()
    slug = AutoSlugField(null=True, default=None, unique=True, populate_from='title')
    added = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    num_views = models.IntegerField(null=True)

    def __str__(self):
        return f'Post: {self.title}'

    class Meta:
        ordering = ['-added']

    @property
    def formatted_markdown(self):
        return markdownify(self.body)


    @property
    def body_summary(self):
        if len(self.body) > 300:
            return markdownify(f'{self.body[:300]}...')
        else:
            return markdownify(self.body)


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
