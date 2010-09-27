# -*- coding: utf-8 -*-
# Create your views here.
from django.http import Http404, HttpResponseRedirect, QueryDict,HttpResponse
from django.conf.urls.defaults import *
from django.db.models import Q
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404,get_list_or_404
from django.contrib.auth.models import User
from django.forms.util import ErrorList
from django.utils import html
from django.core import urlresolvers
from django.views.generic.list_detail import object_list
from django.template import loader, RequestContext

from manager import PostManager
from  models import Post,Categories as Cate  
from  utils import get_pagenum

from django.utils import simplejson

from voting.models import Vote
from django.views.decorators.http import require_POST
def postList(request):
    page = get_pagenum(request)
    posts =  Post.objects.all_by_type(request.path.split("/")[1])
    return  render_to_response('post/post_list.html', {
                    'posts': posts,
                    'page': page,
                    }, context_instance=RequestContext(request)
                )



def postView(request,slug):
    page = get_pagenum(request)
    post = get_object_or_404(Post, slug=slug)
    post.hit_views()
    return render_to_response('post/post_view.html', {
                    'post': post,
                    'page': page,
                    }, context_instance=RequestContext(request)
                )

def catePosts(request,slug):
    page = get_pagenum(request)
    cate=Cate.objects.select_related().get(slug=slug)
    path1=request.path.split("/")[1]
    posts =get_list_or_404(cate.posts.all_by_type(path1))
    return  render_to_response('post/catepost_list.html', {
                    'posts': posts,
                    'page': page,'cate':cate
                    }, context_instance=RequestContext(request)
                )
def test(request):
    values=request.META.items()
    html=[]
    for k,v in values:
        html.append('<tr><td>key : %s</td> <td>%s</td></tr>' % (k,v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))


def vote(request):
    results = {'success':False}
    if request.method == u'GET':
        GET = request.GET
        if GET.has_key(u'pk') and GET.has_key(u'vote'):
            pk = int(GET[u'pk'])
            vote = GET[u'vote']
            post = Post.objects.get(pk=pk)
            if vote == u"up":
                print "^"
                #post.up()
            elif vote == u"down":
                print ">"
                #post.down()
            results = {'success':True}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

VOTE_DIRECTIONS = (('up', 1), ('down', -1), ('clear', 0))

def vote_on_object(request, model, direction, post_vote_redirect=None,
        object_id=None, slug=None, slug_field=None, template_name=None,
        template_loader=loader, extra_context=None, context_processors=None,
        template_object_name='object', allow_xmlhttprequest=False):
    if allow_xmlhttprequest and request.is_ajax():
        return xmlhttprequest_vote_on_object(request, model, direction,
                                             object_id=object_id, slug=slug,
                                             slug_field=slug_field)

    if extra_context is None: extra_context = {}
    if not request.user.is_authenticated():
        return redirect_to_login(request.path)

    try:
        vote = dict(VOTE_DIRECTIONS)[direction]
    except KeyError:
        raise AttributeError("'%s' is not a valid vote type." % vote_type)

    # Look up the object to be voted on
    lookup_kwargs = {}
    if object_id:
        lookup_kwargs['%s__exact' % model._meta.pk.name] = object_id
    elif slug and slug_field:
        lookup_kwargs['%s__exact' % slug_field] = slug
    else:
        raise AttributeError('Generic vote view must be called with either '
                             'object_id or slug and slug_field.')
    try:
        obj = model._default_manager.get(**lookup_kwargs)
    except ObjectDoesNotExist:
        raise Http404, 'No %s found for %s.' % (model._meta.app_label, lookup_kwargs)

    if request.method == 'POST':
        if post_vote_redirect is not None:
            next = post_vote_redirect
        elif request.REQUEST.has_key('next'):
            next = request.REQUEST['next']
        elif hasattr(obj, 'get_absolute_url'):
            if callable(getattr(obj, 'get_absolute_url')):
                next = obj.get_absolute_url()
            else:
                next = obj.get_absolute_url
        else:
            raise AttributeError('Generic vote view must be called with either '
                                 'post_vote_redirect, a "next" parameter in '
                                 'the request, or the object being voted on '
                                 'must define a get_absolute_url method or '
                                 'property.')
        Vote.objects.record_vote(obj, request.user, vote)
        return HttpResponseRedirect(next)
    else:
        if not template_name:
            template_name = '%s/%s_confirm_vote.html' % (
                model._meta.app_label, model._meta.object_name.lower())
        t = template_loader.get_template(template_name)
        c = RequestContext(request, {
            template_object_name: obj,
            'direction': direction,
        }, context_processors)
        for key, value in extra_context.items():
            if callable(value):
                c[key] = value()
            else:
                c[key] = value
        response = HttpResponse(t.render(c))
        return response

def json_error_response(error_message):
    return HttpResponse(simplejson.dumps(dict(success=False,
                                              error_message=error_message)))

def xmlhttprequest_vote_on_object(request, model, direction,
    object_id=None, slug=None, slug_field=None):
 
    if request.method == 'GET':
        return json_error_response(
            'XMLHttpRequest votes can only be made using POST.')
    if not request.user.is_authenticated():
        return json_error_response('Not authenticated.')

    try:
        vote = dict(VOTE_DIRECTIONS)[direction]
    except KeyError:
        return json_error_response(
            '\'%s\' is not a valid vote type.' % direction)

    # Look up the object to be voted on
    lookup_kwargs = {}
    if object_id:
        lookup_kwargs['%s__exact' % model._meta.pk.name] = object_id
    elif slug and slug_field:
        lookup_kwargs['%s__exact' % slug_field] = slug
    else:
        return json_error_response('Generic XMLHttpRequest vote view must be '
                                   'called with either object_id or slug and '
                                   'slug_field.')
    try:
        obj = model._default_manager.get(**lookup_kwargs)
    except ObjectDoesNotExist:
        return json_error_response(
            'No %s found for %s.' % (model._meta.verbose_name, lookup_kwargs))

    # Vote and respond
    Vote.objects.record_vote(obj, request.user, vote)
    return HttpResponse(simplejson.dumps({
        'success': True,
        'score': Vote.objects.get_score(obj),
    }))
