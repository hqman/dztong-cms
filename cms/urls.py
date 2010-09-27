from django.conf.urls.defaults import *



urlpatterns = patterns('cms.views',
     url(r'^$', 'postList'),
	 url(r'^cate/(?P<slug>\w+)/$', 'catePosts',name='postCate'),
	 url(r'^(?P<slug>\w+)/$', 'postView',name='postView'),
)

