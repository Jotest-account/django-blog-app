import uuid

from django.db import models
from django_extensions.db.fields import AutoSlugField


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


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    name = models.CharField(max_length=100)
    text = models.TextField()
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment: {self.id} to Post: {self.post.title}'

    class Meta:
        ordering = ['added']
