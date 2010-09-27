# -*- coding: utf-8 -*-
# Create your views here.
from django.http import Http404, HttpResponseRedirect, QueryDict
from django.conf.urls.defaults import *
from django.db.models import Q
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404,get_list_or_404
from django.contrib.auth.models import User
from django.forms.util import ErrorList
from django.utils import html
from django.core import urlresolvers



from django.contrib.auth import authenticate, login

def login_view(request,template_name):
    if request.user:
        redirect_to = request.REQUEST.get('redirect_to', '/')
        
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                redirect_to = request.REQUEST.get('redirect_to', '/')
            else:
                redirect_to = request.REQUEST.get('redirect_to', '/')
        else:
            redirect_to = request.REQUEST.get('redirect_to', '/')
    else:
        return render_to_response(template_name, {
        redirect_field_name: redirect_to,
         }, context_instance=RequestContext(request))
        
        
        
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
