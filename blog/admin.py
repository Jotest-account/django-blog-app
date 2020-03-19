from django.contrib import admin
from django.db import models
from martor.models import MartorField
from martor.widgets import AdminMartorWidget

from .models import Post, BlogSettings


class PostAdmin(admin.ModelAdmin):
    # fields = ('title',  'slug')
    formfield_overrides = {
        MartorField: {'widget': AdminMartorWidget},
        models.TextField: {'widget': AdminMartorWidget}
    }
    readonly_fields = ('slug',)
    list_display = ('title',  'slug')


admin.site.register(Post, PostAdmin)
admin.site.register(BlogSettings)