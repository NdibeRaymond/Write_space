from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post
from django.urls import reverse





class LatestPostsFeed(Feed):
    title = "Raymond's Writing Space"
    link = ""
    description = "WriteSpace latest blog posts update"

    def items(self):
        return Post.objects.order_by('-publish_date')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.text, 30)

    def item_link(self, item):
        return reverse("posts:post_detail", args=[item.pk])
