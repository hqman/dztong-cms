from django.conf.urls.defaults import *

urlpatterns = patterns('dztong.comment.views',
    url(r'^post/$',          'comments.post_comment',       name='comments-post-comment'),
     (r'^quote_comment$','comments.quote_comment')

)

urlpatterns += patterns('',
    url(r'^cr/(\d+)/(.+)/$', 'django.views.defaults.shortcut', name='comments-url-redirect'),
)

