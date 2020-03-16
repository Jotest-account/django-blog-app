from django.contrib.syndication.views import Feed
from django.urls import reverse
from blog.models import Post


class LatestEntries(Feed):
    title = "J-Os Blogfeed"
    link = "/rss/"
    description = "The latest posts on J-O's blog"

    def items(self):
        return Post.objects.order_by('-added')[:5]

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        # return reverse('post_detail', args=[item.pk])
        return item.get_absolute_url()


