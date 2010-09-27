# coding: utf-8
import datetime
from django.utils.translation import gettext as _
from django.template import Library
from django.db import connection
from cms.models import Post, Categories as Cate
from django.template.loader import render_to_string
from django import template
from django.template import Context
from dztong.urls import urlpatterns


register = Library()


@register.inclusion_tag('sidebar/category_list.html', takes_context = True)
def get_categories(context):
    return {'categories': Cate.objects.all()}


@register.inclusion_tag('sidebar/recent_posts.html', takes_context = True)
def get_recent_posts(context):
    #TODO Use settings to determine the latest items.
    return {'posts': Post.objects.all()[:5]}


@register.tag
def get_cates(parser, token):
    args = token.split_contents()
    template_tag = args[0]
    if len(args) < 2:
        raise template.TemplateSyntaxError, "%r tag requires at least one argument" % template_tag
    return getcateNode(args[1])

class getcateNode(template.Node):
    def __init__(self, url):
        self.url = url

    def render(self, context):
        t = template.loader.get_template('sidebar/category_list.html')
        print "xxxxxxxxx %s",self.url
        return t.render(Context( {'categories': Cate.objects.all(),'post_type':self.url}))


