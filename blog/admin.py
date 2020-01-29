from django.contrib import admin

from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    fields = ('title', 'text', 'slug')
    readonly_fields = ('slug',)
    list_display = ('title', 'text', 'slug')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
