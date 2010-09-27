# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage

register = template.Library()

OBJECTS_PER_PAGE = getattr(settings, 'OBJECTS_PER_PAGE', 8)


#得到 前3页 和后3页     1 2 3 【4】  5 6 7 (1,7)
def get_page_range(current, range):
    if range[-1] < 5:
        return xrange(1, len(range)+1)

    if current-3>=1:
        first=current-3
    else:
        first=1

    if current+3<=range[-1]:
        last=current+4
    else:
        last=range[-1]+1
    return xrange(first, last)

class PaginationNode(template.Node):
    def __init__(self, objects, page, per_page = OBJECTS_PER_PAGE):
        self.object_var_name = objects 
        self.per_page = int(per_page)
        self.objects_to_be_paginated = template.Variable(objects)
        self.current_page = template.Variable(page)

    def render(self, context):
        objects = self.objects_to_be_paginated.resolve(context)
        current = int(self.current_page.resolve(context))
        pagi = Paginator(objects, self.per_page)
        try:
            if current==0:
                current=pagi.num_pages
            page = pagi.page(current)
        except EmptyPage:
            context[self.object_var_name] = None
            context['pagi_page'] = None
            context['pagi_current'] = current
            context['pagi_range'] = None
        else:
            context[self.object_var_name] = page.object_list
            context['pagi_page'] = page
            context['pagi_current'] = current
            context['pagi_range'] = get_page_range(current, pagi.page_range)
        return ''

@register.tag
def pre_pagination(parser, token):
    try:
        tag_name, objects, page, per_page = token.split_contents()
        return PaginationNode(objects, page, per_page)
    except:
        tag_name, objects, page = token.split_contents()
        return PaginationNode(objects, page)
	
#添加时候显示  show_first...  show_last...    
@register.inclusion_tag('pagination/pagination.html', takes_context = True)
def do_pagination(context):
    rs={
            'pagi_page': context['pagi_page'],
            'pagi_current': context['pagi_current'],
            'pagi_range': context['pagi_range'],
            }
    current=int(context['pagi_current'])
    pagi=context['pagi_page']
    if current+3<pagi.paginator.num_pages:
         rs['show_last']=True
    else:
         rs['show_last']=False
    if current-3>1:
         rs['show_first']=True
    else:
         rs['show_first']=False
    if 'pagi_path' in context:
        pagi_path = context['pagi_path']
        rs['pagi_path']= pagi_path
    else:
        pagi_path = ''
        rs['pagi_path']= pagi_path
    return rs

@register.inclusion_tag('pagination/pagination_search.html', takes_context = True)
def do_pagination_search(context):
    if 'pagi_path' in context:
        pagi_path = context['pagi_path']
    else:
        pagi_path = ''
    return {
            'pagi_page': context['pagi_page'],
            'pagi_current': context['pagi_current'],
            'pagi_range': context['pagi_range'],
            'pagi_path': pagi_path,
            }
