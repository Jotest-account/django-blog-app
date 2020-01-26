from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    fields = ('title', 'text', 'slug')
    readonly_fields = ('slug',)
    list_display = ('title', 'text', 'slug')


admin.site.register(Post, PostAdmin)
