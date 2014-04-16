from utils import profile_required, hp_profile_required, tnc_required, goal_required
from datetime import datetime, time, timedelta, date

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from membership.models import Member
from blog.models import Entry

def home(request, membership_home_content=None):
	feedback_num = 0

	time_span_new_members = timedelta(days=9)
	time_ago_new_members = datetime.now() - time_span_new_members
	new_member_list = Member.objects.filter(member_since__gte=time_ago_new_members).order_by('member_since')

	time_span_feedback = timedelta(days=9)
	time_ago_feedback = datetime.now() - time_span_feedback	
	feedback_entry_list = Entry.objects.filter(date_update__gte=time_ago_feedback, do_you_want_feedback=True)
	feedback_num = len(feedback_entry_list)
	
	return render_to_response('public_site/home.html', {
	'membership_home_content' : membership_home_content,
	'new_member_list': new_member_list,
	'feedback_entry_list':feedback_entry_list, 'feedback_num':feedback_num,
	}, context_instance=RequestContext(request))


def aboutus(request):

	return render_to_response('public_site/aboutus.html', {
	
	}, context_instance=RequestContext(request))
	

def news(request):

	return render_to_response('public_site/news.html', {
	
	}, context_instance=RequestContext(request))


def nutrition(request):

	return render_to_response('public_site/nutrition.html', {
	
	}, context_instance=RequestContext(request))

def exercise(request):

	return render_to_response('public_site/exercise.html', {
	
	}, context_instance=RequestContext(request))

def hp(request):

	return render_to_response('public_site/hp.html', {
	
	}, context_instance=RequestContext(request))

def faq(request):

	return render_to_response('public_site/faq.html', {
	
	}, context_instance=RequestContext(request))