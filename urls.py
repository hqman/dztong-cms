from django.conf.urls.defaults import *
from django.conf import settings
from django.views.decorators.cache import cache_page  
from cms.models import Post
from cms.views import vote_on_object

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^dztong/', include('dztong.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': settings.MEDIA_ROOT}),
    url(r'^news/', include('cms.urls'),name='news'),

    url(r'^video/', include('cms.urls'),name='video'),
     url(r'^wiki/', include('cms.urls'),name='wiki'),
    url(r'^$', 'cms.views.postList',name='home'),
   (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    (r'^accounts/logout/$', 'cms.accountViews.logout_view' ),
    (r'^comments/', include('dztong.comment.urls')),

      url(r'^test$', 'cms.views.test',name='home'),

      # Generic view to vote on Link objects


#     Generic view to vote on Link objects
    (r'^vote/(?P<object_id>\d+)/(?P<direction>up|down|clear)/?$',
        vote_on_object, dict(model=Post, template_object_name='Post',
            allow_xmlhttprequest=True)),
)

from dztong.cms.feeds import LatestEntriesFeed ,CatePostsFeed

feeds = {
    'latest': LatestEntriesFeed,
    'cates': CatePostsFeed,
}

urlpatterns =urlpatterns+ patterns('',
    (r'^feeds/(?P<url>.*)/$',  'django.contrib.syndication.views.feed' ,
        {'feed_dict': feeds}),
)

