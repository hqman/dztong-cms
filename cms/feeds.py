# -*- coding: utf-8 -*-
# dztong RSS feed

from django.utils.feedgenerator import Atom1Feed
from django.contrib.sites.models import Site
from django.contrib.syndication.feeds import Feed
from dztong.cms.models import Post,Categories

from django.core.exceptions import ObjectDoesNotExist


current_site = Site.objects.get_current()


class LatestEntriesFeed(Feed):
    author_name = "hqman"
    copyright = "http://%s/about/copyright/" % current_site.domain
    description = "Latest entries posted to %s" % current_site.name
    feed_type = Atom1Feed
    item_copyright = "http://%s/about/copyright/" % current_site.domain
    item_author_name = "hqman"
    item_author_link = "http://%s/" % current_site.domain
    link = "/feeds/posts/"
    title = "%s: Latest entries" % current_site.name
    
    def items(self):
        return Post.objects.all().order_by('-post_date')[:15]
    
    def item_pubdate(self, item):
        return item.post_date
    
    def item_categories(self, item):
        return [c.name for c in item.category.all()]
    
    
class  CatePostsFeed(LatestEntriesFeed):
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Categories.objects.get(slug__exact=bits[0])
    
    def title(self, obj):
        return "%s: Latest entries in category '%s'" % (current_site.name,
         obj.name)
    def description(self, obj):
        return "%s: Latest entries in category '%s'" % (current_site.name,
                                                        obj.name)
    def link(self, obj):
        return obj.get_absolute_url()
    def items(self, obj):
        return obj.posts.order_by('-post_date')[:15]

    
     
     












