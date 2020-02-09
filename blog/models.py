import uuid

from django.db import models
from django_extensions.db.fields import AutoSlugField
from django_comments.moderation import CommentModerator, moderator


class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    slug = AutoSlugField(null=True, default=None, unique=True, populate_from='title')
    added = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Post: {self.title}'

    class Meta:
        ordering = ['-added']
        # db_table = 'categories'
        # verbose_name_plural = 'Categories'


class PostModerator(CommentModerator):
    email_notification = True


moderator.register(Post, PostModerator)
