# -*- coding: utf-8 -*-
from django import http 
from django.http import Http404, HttpResponseRedirect, QueryDict,HttpResponse
from django.conf import settings
from utils import next_redirect, confirmation_view
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.html import escape
from django.views.decorators.http import require_POST
from django.utils import simplejson
 
import logging
from dztong.comment.signals import comment_was_posted
from django.views.decorators.csrf import csrf_protect
from dztong.comment.models import DZComment
from dztong.comment.forms import CommentForm
from django.http import HttpResponseRedirect


class CommentPostBadRequest(http.HttpResponseBadRequest):
    """
    Response returned when a comment post is invalid. If ``DEBUG`` is on a
    nice-ish error message will be displayed (for debugging purposes), but in
    production mode a simple opaque 400 page will be displayed.
    """
    def __init__(self, why):
        super(CommentPostBadRequest, self).__init__()
        if settings.DEBUG:
            self.content = render_to_string("comments/400-debug.html", {"why": why})
            
            
def quote_comment(request):
    results = {'success':False}
    if request.method == u'GET':
        GET = request.GET
        if GET.has_key(u'pk'):
            
            pk = int(GET[u'pk'])
            
            comment=DZComment.objects.get(pk=pk)
           
            results = {'success':True,'content':comment.content,'author':comment.user_name}
            
    json = simplejson.dumps(results)
    print 'hh %s' % json
    return HttpResponse(json, mimetype='application/json')

    
        


@require_POST
def post_comment(request):
    data = request.POST.copy()
    if request.user.is_authenticated():
        if not data.get('user_name', ''):
            try:
                data['user_name'] = request.user.get_profile().nickname
            except:
                data['user_name'] = request.user.get_full_name() or request.user.username

    # Look up the object we're trying to comment about
    ctype = data.get("content_type")
    object_pk = data.get("object_pk")

    if ctype is None or object_pk is None:
        return CommentPostBadRequest("Missing content_type or object_pk field.")

    try:
        model = models.get_model(*ctype.split(".", 1))
        target = model._default_manager.get(pk=object_pk)
    except TypeError:
        return CommentPostBadRequest(
            "Invalid content_type value: %r" % escape(ctype))
    except AttributeError:
        return CommentPostBadRequest(
            "The given content-type %r does not resolve to a valid model." % \
                escape(ctype))
    except ObjectDoesNotExist:
        return CommentPostBadRequest(
            "No object matching content-type %r and object PK %r exists." % \
                (escape(ctype), escape(object_pk)))

    # Construct the comment form
    form = CommentForm(target, data=data)
    # Check security information
    if form.security_errors():
        return CommentPostBadRequest(
            "The comment form failed security verification: %s" % \
                escape(str(form.security_errors())))

    # If there are errors
    if form.errors:
        message = None
        for field in ['author', 'email', 'content', 'url']:
            if field in form.errors:
                if form.errors[field][0]:
                    message = '[%s] %s' % (field.title(), form.errors[field][0].capitalize())
                    break

        return render_to_response('post/error.html', {'message': message})
    comment = form.get_comment_object()
    comment.parent_id = data['parent_id']
    comment.user_name = data['user_name']
    comment.ip_address = request.META.get("REMOTE_ADDR", None)
    if request.user.is_authenticated():
        comment.user = request.user
    #print  comment.content_type
    # Signal that the comment is about to be saved
    '''responses = signals.comment_p.send(
        sender  = comment.__class__,
        comment = comment,
        request = request
    )

    for (receiver, response) in responses:
        if response == False:
            return CommentPostBadRequest(
                "comment_will_be_posted receiver %r killed the comment" % receiver.__name__)'''

    # Save the comment and signal that it was saved
    comment.save()
#    comment_was_posted.send(
#        sender  = comment.__class__,
#        comment = comment,
#        request = request
#    )
    return HttpResponseRedirect('%s?page=0#comment-%d' % (target.get_absolute_url(), comment.id))
 
