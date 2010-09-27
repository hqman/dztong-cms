# -*- coding: utf-8 -*-
import datetime
from django.core.cache import cache
from django.db import connection, transaction
from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from manager import CategoriesManager,PostManager
from dztong.comment.models import DZComment
from  dztong.comment import signals

from dztong.cms.thumbs import ImageWithThumbsField



# 文章系统模型定义，参考wordpress表结构

TABLE_PREFIX="dztong"

COMMENT_CLOSE=1
COMMENT_OPEN=2

STATUS_CHOICES = (
    (COMMENT_CLOSE, 'closed'),
    (COMMENT_OPEN, 'open'),
)

POST_DRAFT=1
POST_MODERATED=2
POST_APPROVED=3
POST_SPAM=4
POST_TRASH=5

"""
moderated 未审核
approved  通过
spam       垃圾
trash  进入回收站"""

POST_STATUS_CHOICES = (
    (POST_DRAFT, '草稿'),
    (POST_APPROVED, '审核通过'),
    (POST_MODERATED,'未审核'),
    (POST_SPAM, '垃圾新闻'),
    (POST_TRASH, '回收站'),
)

NEWS_CREATE=1
NEWS_COPY=2
NEWS_TRANS=3

NEWS_TYPES=(
    (NEWS_CREATE,'原创'),
    (NEWS_COPY,'转载'),
    (NEWS_TRANS,'翻译'),
)

POST_TYPES=(
     (1,"news"),
     (2,"wiki"),
     (3,"video"),
)

POST_TYPES_DIC={1:'news',2:'wiki',3:'video'}




class Categories(models.Model):
    """
    文章分类
    """
    objects=CategoriesManager()
    #id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True)
    description= models.TextField(blank=True)
    #parent = models.IntegerField(default=0)
    parent = models.ForeignKey('self',default=0 ,blank = True, null = True)
    postCount = models.IntegerField(default=0,editable=False)


    class Meta:
        db_table = '%s_cate' % TABLE_PREFIX
        ordering = ['id',]
        verbose_name_plural='文章分类'

    def __unicode__(self):
        return self.name

    #@models.permalink


    def get_absolute_url(self):
         return "%s/" %  self.slug






class Post(models.Model):
    """
    The mother lode.
    The WordPress post.
    """
    objects=PostManager()

    # post data
    #guid = models.CharField(max_length=255)
    news_type = models.IntegerField(blank=True,  choices=NEWS_TYPES,default=NEWS_CREATE)
    status = models.IntegerField(max_length=4,  choices=POST_STATUS_CHOICES,default=POST_MODERATED)
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=200)
    author = models.ForeignKey(User, related_name='posts' )
    excerpt = models.TextField()
    content = models.TextField()
    comments =  generic.GenericRelation(DZComment,
                    object_id_field='object_primary_key',
                    content_type_field='content_type_fk')
    #content_filtered = models.TextField()
    post_date = models.DateTimeField(default=datetime.datetime.now,auto_now_add=True, )
    modified = models.DateTimeField(default=datetime.datetime.now,auto_now_add=True, )

    # comment stuff
    comment_status = models.IntegerField(max_length=4, choices=STATUS_CHOICES,default=COMMENT_OPEN)
    comment_count = models.IntegerField(default=0,editable=False)
    view_count = models.IntegerField(default=0,help_text='点击量',verbose_name='点击量')
    category = models.ManyToManyField(Categories,related_name="posts")
    from_url = models.URLField(blank=True, verify_exists=False,max_length=300,help_text='来源网址')
    from_site = models.CharField(blank=True, max_length=200,help_text='来源网站')
    post_type = models.IntegerField(max_length=2,choices=POST_TYPES)
    #image= ImageWithThumbsField(upload_to="photos",sizes=((125,125),(200,200)))



    def save(self):
        try:
            self.content = html.clean_html(self.content)
        except:
            pass
        super(Post, self).save()

        # call cache sweeper to clear releate caches
        #PostSweeper.after_save(self)

        # Initial the views and comments count to 0 if the PostMeta isn't available
        pm, created = PostMeta.objects.get_or_create(post=self, meta_key='views')
        if created:
            pm.meta_value = '0'
            pm.save()

        pm, created = PostMeta.objects.get_or_create(post=self, meta_key='comments_count')
        if created:
            pm.meta_value = '0'
            pm.save()


    def __unicode__(self):
        return self.title

    def get_author(self):
        cache_key = 'models/user/%s' % self.id
        username = cache.get(cache_key)
        if not username:
            try:
                profile = self.author.get_profile()
            except Exception:
                cache.set(cache_key,self.author.username)
            else:
                cache.set(cache_key,profile.nickname)
        return username

    def get_view_count(self):
        return self.view_count
        #return PostMeta.objects.get(post=self, meta_key='views').meta_value

    def get_comment_count(self):
         return self.comment_count


    @transaction.commit_on_success
    def hit_comments(self):
        cursor = connection.cursor()
        cursor.execute("update dztong_post  set comment_count=comment_count+1 where id=%s" % self.id)
        transaction.commit_unless_managed()

    @transaction.commit_on_success
    def hit_views(self):
        cursor = connection.cursor()
        cursor.execute("update dztong_post  set view_count=view_count+1 where id=%s" % self.id)
        transaction.commit_unless_managed()

#    def get_view_count(self):
#        cache_key = 'models/post/view_count/%s' % self.id
#        view_count = cache.get(cache_key)
#        if not view_count:
#            cache.set(cache_key,self._get_views_count)
#        return view_count





#    def get_comment_count(self):
#        cache_key = 'models/post/comment_count/%s' % self.id
#        comment_count_cache=cache.get(cache_key)
#        if not comment_count_cache :
#             cache.set(cache_key,self._get_comments_countsl)
#        else:
#            return comment_count_cache

    """
    @models.permalink
    def get_absolute_url(self):
        return  ('postView',None,{'slug':self.slug})
            """

    #@models.permalink
    def get_absolute_url(self):
         return "/%s/%s/" % (POST_TYPES_DIC[self.post_type],self.slug)

    def get_categories(self):
        return self.category.all()



    class Meta:
        db_table = '%s_post' % TABLE_PREFIX
        ordering = ['id',]
        verbose_name_plural='文章'


class PostMeta(models.Model):
    post = models.ForeignKey(Post)
    meta_key = models.CharField(max_length=128)
    meta_value = models.TextField()

    def __unicode__(self):
        return '<%s: %s>' % (self.meta_key, self.meta_value)




class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)

    nickname = models.CharField(max_length=30)
    #website = models.URLField(blank=True)

    def save(self):
        if not self.nickname:
            self.nickname = self.user.username
        super(Profile, self).save()

    def __unicode__(self):
        return self.nickname

#class   Comment(models.Model):


def on_comment_save(sender, comment, *args, **kwargs):
    post =comment. object
    print type(object)
    post.hit_comments()

signals.comment_save.connect(on_comment_save)

