#!/usr/bin/python

from django.utils.feedgenerator import Atom1Feed
from django.contrib.sites.models import Site
from django.contrib.syndication.feeds import Feed
from coltrane.models import Entry

current_site = Site.objects.get_current()

class LatestEntriesFeed(Feed):
    """My custom RSS feed"""
    author_name = "Michael Ruggiero"
    copyright = "http://%s/about/copywright/" % current_site.domain
    feed_type = Atom1Feed
    item_copyright = "http://%s/about/copywright/" % current_site.domain
    item_author_name = "Michael Ruggiero"
    item_author_link = "http://%s/" % current_site.domain

    link = "/feeds/entries/"
    title = "%s: Latest Entries" % current_site.name
        
    def items(self, item):
        """docstring for items"""
        return Entry.live.all()[:15]

    def item_pubdate(self, item):
        """docstring for item_pubdate"""
        return item.pub_date

    def item_guid(self, item):
        """docstring for item_guid"""
        return "tag:%s,%s:%s" % (current_site.domain, 
                                  item.pub_date.strftime('%Y-%m-%d'), 
                                  item.get_absolute_url()) 

    def item_categories(self, item):
        """docstring for item_categories"""
        return [ c.title for c in item.categories.all() ]
