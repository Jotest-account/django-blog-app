from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from blog.views import markdown_uploader
from . import views
from .feeds import LatestEntries

urlpatterns = [
                  # django admin
                  path('admin/', admin.site.urls),
                  # user management
                  path('accounts/', include('allauth.urls')),
                  path('user_profile/<int:pk>', views.UserUpdate.as_view(), name='user_edit'),
                  # local apps
                  path('', include('pages.urls')),
                  path('blog/', include('blog.urls')),
                  path('rss/', LatestEntries()),
                  path('martor/', include('martor.urls')),
                  path('api/uploader/', markdown_uploader, name='markdown_uploader_page'
                       ),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
