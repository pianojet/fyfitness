from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
import urllib
from membership.models import Member, HealthProfessional, Goal

from django.utils.safestring import mark_safe
from django import template

register = template.Library()

@register.filter
def dictsafe(x):
	return mark_safe(dictsafe_impl(x))
dictsafe.is_safe = True

def dictsafe_impl(x):
	if x == None:
		return 'null'
	if isinstance(x, str) or isinstance(x, unicode):
		return "'%s'"%str(x).replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")
	elif hasattr(x, 'keys') and hasattr(x, '__getitem__'):
		return "{%s}"%','.join(["%s:%s"%(dictsafe_impl(i),dictsafe_impl(x[i])) for i in x.keys()])
	elif hasattr(x, '__getitem__'):
		return "[%s]"%','.join([ dictsafe_impl(i) for i in x ])
	else:
		return '%s'%x


	

def profile_required(f):
	
	def wrap(request, *args, **kwargs):
		if (request.user.is_authenticated):
			me = Member.objects.filter(user=request.user)
			if (len(me) == 0):
				return HttpResponseRedirect('/membership/create_profile/?%s'%urllib.urlencode({'next':request.get_full_path()}))

		return f(request, *args, **kwargs)

	wrap.__doc__=f.__doc__
	wrap.__name__=f.__name__
	return wrap
	
def hp_profile_required(f):
	
	def wrap(request, *args, **kwargs):
		if (request.user.is_authenticated):	
			me = Member.objects.filter(user=request.user)

			hp = HealthProfessional.objects.filter(member=me)
			if (len(hp) == 0 and me[0].i_am_a_health_professional == True):
				return HttpResponseRedirect('/membership/create_hp_profile/?%s'%urllib.urlencode({'next':request.get_full_path()}))

		return f(request, *args, **kwargs)
		
	wrap.__doc__=f.__doc__
	wrap.__name__=f.__name__
	return wrap
	
def tnc_required(f):
	
	def wrap(request, *args, **kwargs):
		if (request.user.is_authenticated):	
			me = Member.objects.filter(user=request.user)
			if (me[0].i_accept_terms_and_conditions == False):
				return HttpResponseRedirect('/membership/accept_tnc/?%s'%urllib.urlencode({'next':request.get_full_path()}))
		return f(request, *args, **kwargs)
		
	wrap.__doc__=f.__doc__
	wrap.__name__=f.__name__
	return wrap
	
def goal_required(f):
	
	def wrap(request, *args, **kwargs):
		if (request.user.is_authenticated):	
			g = Goal.objects.filter(member__user=request.user, primary_goal=True)
			if (len(g) == 0):
				return HttpResponseRedirect('/membership/create_goal/?%s'%urllib.urlencode({'next':request.get_full_path()}))
		return f(request, *args, **kwargs)
		
	wrap.__doc__=f.__doc__
	wrap.__name__=f.__name__
	return wrap
	

words_avoided = [ "fucker", "fuck", "shit", "piss", "bitch", "cunt", "cock", "nigger", "nigga", "wanker", "faggot", "slut"]
