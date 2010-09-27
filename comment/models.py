# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from dztong.comment.manager import DZCommentManager

from django.conf import settings

from django.utils.encoding import smart_str
from dztong.comment.signals  import comment_was_posted,comment_save
 
from akismet import Akismet
from akismet import AkismetError

COMMENT_MAX_LENGTH = ('COMMENT_MAX_LENGTH', 3000)
COMMENT_MAX_DEPTH = ( 'COMMENT_MAX_DEPTH', 5)


class DZComment(models.Model):
    """
    A user comment about some object.
    """
    content_type   = models.ForeignKey(ContentType)
#            related_name="content_type_set_for_%(class)s")
    object_pk      = models.PositiveIntegerField(('object id'))
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")
    # Who posted this comment? If ``user`` is set then it was an authenticated
    # user; otherwise at least user_name should have been set and the comment
    # was posted by a non-authenticated user.
    user        = models.ForeignKey(User, blank=True, null=True)
#            related_name="%(class)s_comments")
    user_name   = models.CharField(("user's name"), max_length = 50, blank = True)
    content = models.TextField(('内容'), max_length=COMMENT_MAX_LENGTH)
    parent = models.ForeignKey('self', null = True,
                                       blank = True,
                                       default = None,
                                       related_name = 'children')

    # Metadata about the comment
    ip_address  = models.IPAddressField(('IP 地址 '), blank=True, null=True)
    submit_date = models.DateTimeField(('发布时间'), default=datetime.datetime.now,auto_now_add=True,)
    is_public   = models.BooleanField(('是否公开'), default=True)
    is_removed  = models.BooleanField(('是否删除'), default=False)
    site        = models.ForeignKey(Site, related_name="comment for %(class)s")

     # Manager
    objects = DZCommentManager()

    class Meta:
        ordering = ('submit_date',)

    def get_content_object_url(self):
        """
        Get a URL suitable for redirecting to the content object.
        """
        model = ContentType.objects.get(pk = self.content_type_id).model_class()
        object = model.objects.get(pk = self.object_pk)
        return object.get_absolute_url()

    def get_absolute_url(self, anchor_pattern="#comment-%(id)s"):
        return self.get_content_object_url() + (anchor_pattern % self.__dict__)

    def __unicode__(self):
        return " %s..." %  self.content[:50]
    def _get_object(self):
        model = ContentType.objects.get(pk = self.content_type_id).model_class()
        object = model.objects.get(pk = self.object_pk)
        return object
    object = property(_get_object)
    
    def save(self):
        super(DZComment, self).save()
         
        comment_save.send(sender = self.__class__, comment = self, object =object)



 




 
def on_comment_was_posted(sender, comment, request, *args, **kwargs):
    try:
        from akismet import Akismet
        from akismet import AkismetError
    except:
        return

    if hasattr(settings, 'AKISMET_API_KEY'):
        ak = Akismet(
            key = settings.AKISMET_API_KEY,
            blog_url='http://%s/' % Site.objects.get(pk=settings.SITE_ID).domain
        )
    else:
        print("no AKISMET_API_KEY")
        return

    try:
        if ak.verify_key():
            print "key is valid"
            data = {
                'user_ip': request.META.get('REMOTE_ADDR', '127.0.0.1'),
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                'referrer': request.META.get('HTTP_REFERER', ''),
                'comment_type': 'comment',
                'comment_author': comment.user_name.encode('utf-8'),
            }

            if ak.comment_check(smart_str(comment.content), data=data, build_data=True):
                comment.is_public = False
                comment.save()
    except AkismetError:
        print "key not valid"
        comment.save() 
        
comment_was_posted.connect(on_comment_was_posted)
 

