from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from .models import Post


class PostAdmin(MarkdownxModelAdmin):
    fields = ('title', 'text', 'slug')
    readonly_fields = ('slug',)
    list_display = ('title', 'text', 'slug')


admin.site.register(Post, MarkdownxModelAdmin)
