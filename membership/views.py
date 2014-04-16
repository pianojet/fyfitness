from utils import profile_required, hp_profile_required, tnc_required, goal_required, dictsafe

from datetime import datetime, time, timedelta, date

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from public_site.views import home

import urllib

from membership.forms import MemberForm, EditProfile, tncForm
from membership.forms import HealthProfessionalForm
from membership.forms import ProgressForm
from membership.forms import GoalForm
from membership.forms import AcUserForm1, AcUserForm2

from membership.models import Progress, Member, Goal, Follow, HealthProfessional, PROGRESS_PERMS
from blog.models import Entry


def edit_perm(request, object_type, object_id, perm):
	success = True
	try:
		ob = None
		if object_type == "goal":
			ob = Goal.objects.get(id=object_id, member__user=request.user)
		elif object_type == "profile":
			ob = Member.objects.get(id=object_id, user=request.user)
		if len([x for x in PROGRESS_PERMS if x[0] == perm]) > 0:
			ob.who_can_view = perm
			ob.save()
		else:
			success = False
	except:
		success = False
	return HttpResponse('edit_perm_callback({"object_id": %s, "object_type": "%s", "perm": "%s", "success": %s})'%(object_id, object_type, perm, "true" if success else "false"), mimetype="text/javascript")

def return_post_num(request):
	mData = {}
	mData['exists'] = 0
	mData['entry_num'] = 0
	
	me_l = Member.objects.filter(user=request.user)
	if len(me_l) > 0:
		mData['exists'] = 1
		mData['entry_num'] = me_l[0].get_total_new_post_num()
		mData['message_num'] = me_l[0].to_list.filter(read_date=None).count()
	
	mDictSafe = dictsafe(mData)
	
	return HttpResponse("postNumCallback("+mDictSafe+")", mimetype="text/javascript")
	
	
def ajax_follow(request, member_id):
	mData = {}
	mData['src'] = ""
	mData['onclick'] = ""	
	mData['message'] = ""
	mData['title'] = ""
	mData['alt'] = ""
	mData['member_id'] = member_id
	try:
		u = Member.objects.filter(id=member_id)[0]
		me = Member.objects.filter(user=request.user)[0]
		if (Follow.objects.filter(m=me, y=u).count() == 0):
			f = Follow.objects.create(m=me, y=u)
			f.save()
			mData['src'] = "../images/follow_sub.png"
			mData['onclick'] = "sub"
			mData['title'] = "Un-Follow this member"
			mData['alt'] = "Un-Follow this member"
		else:
			mData['src'] = "failure"
			mData['message'] = "There was an error in setting up this Follow.  There may be a bug, please report to fyfitness@gmail.com"
	except:
		mData['src'] = "failure"
		mData['message'] = "There was an error in setting up this Follow.  There may be a bug, please report to fyfitness@gmail.com"
		
	
	mDictSafe = dictsafe(mData)
	return HttpResponse("followCallback("+mDictSafe+")", mimetype="text/javascript")
	

def ajax_auth(request, member_id):
	mData = {}
	mData['src'] = ""
	mData['onclick'] = ""	
	mData['message'] = ""
	mData['title'] = ""
	mData['alt'] = ""
	mData['member_id'] = member_id
	try:
		u = Member.objects.filter(id=member_id)[0]
		me = Member.objects.filter(user=request.user)[0]
		if not(u in me.auth.all()):
			me.auth.add(u)
			me.save()
			mData['src'] = "../images/auth_sub.png"
			mData['onclick'] = "sub"
			mData['title'] = "Un-Authorize this member"
			mData['alt'] = "Un-Authorize this member"
		else:
			mData['src'] = "failure"
			mData['message'] = "There was an error in setting up this authorization.  There may be a bug, please report to fyfitness@gmail.com"
	except:
		mData['src'] = "failure"
		mData['message'] = "There was an error in setting up this authorization.  There may be a bug, please report to fyfitness@gmail.com"
		
	
	mDictSafe = dictsafe(mData)
	return HttpResponse("authCallback("+mDictSafe+")", mimetype="text/javascript")


def ajax_unfollow(request, member_id):
	mData = {}
	mData['src'] = ""
	mData['onclick'] = ""
	mData['message'] = ""
	mData['title'] = ""
	mData['alt'] = ""	
	mData['member_id'] = member_id	
	try:
		u = Member.objects.filter(id=member_id)[0]
		me = Member.objects.filter(user=request.user)[0]

		u_foll = Follow.objects.get(m=me, y=u)
		u_foll.delete()
		mData['src'] = "../images/follow_add.png"
		mData['onclick'] = "add"
		mData['title'] = "Follow this member"
		mData['alt'] = "Follow this member"
	except:
		mData['src'] = "failure"
		mData['message'] = "There was an error in unfollowing this member.  There may be a bug, please report to fyfitness@gmail.com"
		
	
	mDictSafe = dictsafe(mData)
	return HttpResponse("followCallback("+mDictSafe+")", mimetype="text/javascript")
	

def ajax_unauth(request, member_id):
	mData = {}
	mData['src'] = ""
	mData['onclick'] = ""	
	mData['message'] = ""
	mData['title'] = ""
	mData['alt'] = ""
	mData['member_id'] = member_id
	try:
		u = Member.objects.filter(id=member_id)[0]
		me = Member.objects.filter(user=request.user)[0]
		if (u in me.auth.all()):
			me.auth.remove(u)
			me.save()
			mData['src'] = "../images/auth_add.png"
			mData['onclick'] = "add"
			mData['title'] = "Authorize this member"
			mData['alt'] = "Authorize this member"
		else:
			mData['src'] = "failure"
			mData['message'] = "There was an error in unauthorizing this member.  There may be a bug, please report to fyfitness@gmail.com"
	except:
		mData['src'] = "failure"
		mData['message'] = "There was an error in unauthorizing this member.  There may be a bug, please report to fyfitness@gmail.com"
		
	
	mDictSafe = dictsafe(mData)
	return HttpResponse("authCallback("+mDictSafe+")", mimetype="text/javascript")



@login_required
def tnc(request):
	if request.method == 'POST':
		form = tncForm(request.POST)

		if form.is_valid():
			accept = form.cleaned_data['i_accept_terms_and_conditions']
			me = Member.objects.get(user=request.user)
			me.i_accept_terms_and_conditions = accept
			me.save()

			nexturl = '/membership/home/'
			if(request.GET.get('next', False)):
				nexturl = request.GET.get('next')

			return HttpResponseRedirect(nexturl)
	else:
		form = tncForm()
	
	return render_to_response('membership/tnc.html', {
	'form': form,
	}, context_instance=RequestContext(request))

@login_required
@profile_required
@hp_profile_required
@tnc_required
@goal_required
def membership_home(request):
	m_h_c = "<p style='text-align: center; font-size: 30px;'>Welcome, %s</p>"%(request.user.username)
	return home(request, membership_home_content=m_h_c)

@login_required
@profile_required
@hp_profile_required
@tnc_required
@goal_required
def follow(request, f_type=None, member_id=None):


	me = Member.objects.get(user=request.user)
	all_my_auth = me.auth.all()
	all_my_foll = me.follow.all()
	dbmessage = ""
	#dbmessage = "all_my_foll: %s"%(all_my_foll)
	message = ""
	
	if (member_id == None):
		if request.method == 'POST' and f_type == 'auth':
			authForm = AcUserForm1(request.POST)
			follForm = AcUserForm2()
			if authForm.is_valid():
				username = authForm.cleaned_data['an_existent_user1']
				u = Member.objects.get(user=User.objects.get(username=username))
				if (u in all_my_auth):
					message = "%s is already authorized to view your restricted content."%username

				else:
					me.auth.add(u)
					me.save()
					message = "%s added to list of authorized users that can view your restricted content."%username

		elif request.method == 'POST' and f_type == 'follow':
			authForm = AcUserForm1()
			follForm = AcUserForm2(request.POST)
			if follForm.is_valid():
				username = follForm.cleaned_data['an_existent_user2']
				u = Member.objects.get(user=User.objects.get(username=username))
				if (u in all_my_foll):
					message = "You are already following %s."%username
				
				else:
					f = Follow.objects.create(m=me, y=u)
					f.save()
					#me.foll.add(u)
					#me.save()
					
					message = "You are now following %s."%username

		else:
			authForm = AcUserForm1()
			follForm = AcUserForm2()
	else:
		u = Member.objects.get(id=member_id)	
		if (f_type == 'auth'):
			if (u in all_my_auth):
				message = "%s is already authorized to view your restricted content."%u.user.username
			else:
				me.auth.add(u)
				message = "%s added to list of authorized users that can view your restricted content."%u.user.username
		elif(f_type == 'follow'):
			if (u in all_my_foll):
				message = "You are already following %s."%u.user.username
			else:
				f = Follow.objects.create(m=me, y=u)
				f.save()
				message = "You are now following %s."%u.user.username
		elif(f_type == 'remove_auth'):
			if not(u in all_my_auth):
				message = "%s is not authorized to view your restricted content."%u.user.username
			else:
				me.auth.remove(u)
				#u_auth.delete()
				message = "%s is now unable to view your restricted content."%u.user.username		
		else:
			if not(u in all_my_foll):
				message = "You are not following %s."%u.user.username
			else:
				u_foll = Follow.objects.get(m=me, y=u)
				#u_foll = me.follow.get(y=u)
				u_foll.delete()
				message = "You are no longer following %s."%u.user.username		
		authForm = AcUserForm1()
		follForm = AcUserForm2()
		
	all_my_auth = me.auth.all()
	all_my_foll = me.follow.all()	
			
	return render_to_response('membership/follow.html', {
	'all_my_auth':all_my_auth, 'all_my_foll': all_my_foll,
	'message': message,
	'dbmessage': dbmessage,
	'authForm' : authForm, 'follForm' : follForm,
	}, context_instance=RequestContext(request))	



@login_required
def create_profile(request):
	if request.method == 'POST':
		form = MemberForm(request.POST)

		if form.is_valid(): 
			member = form.save(commit=False)
			member.user = request.user
			member.save()

			nexturl = '/membership/home/'
			if(request.GET.get('next', False)):
				nexturl = request.GET.get('next')

			return HttpResponseRedirect(nexturl)
	else:
		form = MemberForm()
	
	return render_to_response('membership/create_profile.html', {
	'form': form,
	}, context_instance=RequestContext(request))

@login_required
@profile_required
def create_hp_profile(request):
	if request.method == 'POST':
		form = HealthProfessionalForm(request.POST)

		if form.is_valid(): 
			hp = form.save(commit=False)
			hp.member = Member.objects.get(user=request.user)
			hp.save()
			nexturl = '/public_site/'
			if(request.GET.get('next', False)):
				nexturl = request.GET.get('next')
			return HttpResponseRedirect(nexturl)
				
	else:
		form = HealthProfessionalForm()	
	
	
	return render_to_response('membership/create_hp_profile.html', {
	'form': form,
	}, context_instance=RequestContext(request))
	
@login_required
@profile_required
@hp_profile_required
@tnc_required
def create_goal(request):
	goals = None
	nexturl = '/public_site/'
	if(request.GET.get('next', False)):
		nexturl = request.GET.get('next')
	
	if request.method == 'POST':
		form = GoalForm(request.POST)

		if form.is_valid(): 
			goal = form.save(commit=False)
			goal.member = Member.objects.get(user=request.user)
			goal.goal_end_date = date(2010, 12, 9)
			if goal.primary_goal:
				for g in Goal.objects.filter(member__user=request.user, primary_goal=True):
					g.primary_goal = False
					g.save()
			goal.save()
			
			progress = Progress(day=datetime.now(), current_stat=form.cleaned_data['starting_unit_number'], member=goal.member, goal=goal)
			progress.save()
			
			if request.POST['submit_type'].find("create") != -1:
				return HttpResponseRedirect("/membership/create_goal/?%s"%urllib.urlencode({'next':nexturl}))
			return HttpResponseRedirect(nexturl)
				
	else:
		form = GoalForm(initial={ "primary_goal": 1-len(Goal.objects.filter(member__user=request.user, primary_goal=True)) })
	
	if len(Goal.objects.filter(member__user=request.user, primary_goal=True)) == 0 and len(Goal.objects.filter(member__user=request.user)) > 0:
		goals = Goal.objects.filter(member__user=request.user)
	return render_to_response('membership/goals.html', {
	'goals': goals,
	'next': urllib.urlencode({'next':nexturl}),
	'form': form,
	}, context_instance=RequestContext(request))	
	
@login_required
@profile_required
@hp_profile_required
@tnc_required
def edit_goal(request, goal_id):
	goals = Goal.objects.filter(id=goal_id)
	if len(goals) == 0:
		return render_to_response('public_site/home.html', {
				'message': 'Error: goal with id %s not found.'%goal_id,
			}, context_instance=RequestContext(request))
	if goals[0].member.user != request.user:
		return render_to_response('public_site/home.html', {
				'message': "Error: cannot edit a goal that isn't yours.",
			}, context_instance=RequestContext(request))
	if not goals[0].can_edit():
		return render_to_response('public_site/home.html', {
				'message': 'Error: cannot edit goals more than 2 weeks old.',
			}, context_instance=RequestContext(request))
	nexturl = '/public_site/'
	if(request.GET.get('next', False)):
		nexturl = request.GET.get('next')
	
	if request.method == 'POST':
		form = GoalForm(request.POST, instance=goals[0])
		
		if form.is_valid(): 
			goal = form.save(commit=False)
			goal.member = Member.objects.get(user=request.user)
			goal.goal_end_date = date(2010, 12, 9)
			if goal.primary_goal:
				for g in Goal.objects.filter(member__user=request.user, primary_goal=True):
					g.primary_goal = False
					g.save()
			goal.save()
			
			progress = Progress.objects.filter(goal=goal).order_by('day')[0]
			progress.current_stat = form.cleaned_data['starting_unit_number']
			progress.save()
			
			if request.POST['submit_type'].find("create") != -1:
				return HttpResponseRedirect("/membership/create_goal/?%s"%urllib.urlencode({'next':nexturl}))
			return HttpResponseRedirect(nexturl)
			
	elif request.GET.get("primary","") == "set":
		goals[0].primary_goal = True;
		goals[0].save()
		return HttpResponseRedirect(nexturl)
	else:
		form = GoalForm(instance=goals[0])
	
	
	return render_to_response('membership/goals.html', {
	'form': form,
	'next': urllib.urlencode({'next':nexturl}),
	}, context_instance=RequestContext(request))	
	
@login_required
@profile_required
@hp_profile_required
@tnc_required
@goal_required
def update_progress(request, goal_id=None):
	message = None
	if goal_id == None:
		goal_id = "0"
	goals = Goal.objects.filter(member__user=request.user).order_by('-primary_goal')
	if request.method == 'POST':
		form = ProgressForm(request.POST)
		form.fields['goal_to_update'].choices = [ (g.id, g.describe(html=False)) for g in goals ]
		
		if form.is_valid():
			progress = Progress(day=datetime.now(), current_stat=form.cleaned_data['current_stat'], member=m, goal=g)
			progress.save()
			message = "Progress saved."			

			form = ProgressForm(initial={"goal_to_update":int(goal_id)})
	else:
		form = ProgressForm(initial={"goal_to_update":int(goal_id)})
	
	form.fields['goal_to_update'].choices = [ (g.id, g.describe(html=False)) for g in goals ]
	
	return render_to_response('membership/progress.html', {
	'message': message,
	'goals': goals,
	'form': form,
	}, context_instance=RequestContext(request))	

@login_required
@profile_required
@hp_profile_required
@tnc_required
@goal_required
def show_profile(request, user_id=None):
	#a member wants to see the information about another member
	
	me = Member.objects.get(user=request.user)
	blog_entries = []
	u = None
	goals = None
	prog = None
	
	hp = None
	dbmessage = ""
	u_profile = {}

	if request.method == 'POST':
		form = AcUserForm1(request.POST)

		if form.is_valid():
			#fill profile vars
			username = form.cleaned_data['an_existent_user1']		
			user_f = User.objects.filter(username=username)
			if (len(user_f) > 0):
				return HttpResponseRedirect("/membership/show_profile/%d/"%user_f[0].id)
				#u_f = Member.objects.filter(user=user_f[0])
				#if (len(u_f) > 0):
				#	return HttpResponseRedirect("/membership/show_profile/%d/"%u_f[0].id)
	elif (user_id != None):
		#fill profile vars
		user_f = User.objects.filter(id=user_id)
		u_f = Member.objects.filter(user=user_f[0])
		if (len(u_f) > 0):
			u = u_f[0]

	if (u):
		if (u.user == request.user or (len(u.auth.filter(id=me.id)) > 0 and u.who_can_view == "Restricted") or u.who_can_view == "Everyone"):
			u_profile['first_name'] = u.first_name
			u_profile['last_name'] = u.last_name
			u_profile['gender'] = u.gender
			u_profile['location'] = u.location
			u_profile['member_since'] = u.member_since
			u_profile['occupation'] = u.occupation
			u_profile['strengths'] = u.strengths
			u_profile['want_support'] = u.want_support
			u_profile['about_me'] = u.about_me

			if (u.i_am_a_health_professional):
				u_profile['is_hp'] = "Yes"
				u_profile['hp_confirmed'] = ""
				u_profile['hp_confirmed'] = "Yes" if (u.hp_confirmed) else "No"

				hp_f = HealthProfessional.objects.filter(member=u)
				if (len(hp_f) > 0):
					hp = hp_f[0]
					u_profile['job_field'] = hp.job_field
					u_profile['job_title'] = hp.job_title
					u_profile['credentials'] = hp.credentials

			else:
				u_profile['is_hp'] = "No"
				u_profile['hp_confirmed'] = "No"
		blog_entries = me.get_new_posts(u.id)
		goals = Goal.objects.filter(member=u)
	
	form = AcUserForm1()
	
	return render_to_response('membership/profile.html', {
	'dbmessage': dbmessage,
	'u_profile' : u_profile,	
	'u': u,
	'goals': goals,
	'form': form,	
	'blog_entries': blog_entries,
	}, context_instance=RequestContext(request))
	

@login_required
@profile_required
@hp_profile_required
@tnc_required
@goal_required
def edit_profile(request):

	message = ""
	me = Member.objects.get(user=request.user)
	me_goal = Goal.objects.get(member=me)
	if request.method == 'POST':
		form = EditProfile(request.POST)

		if form.is_valid():
			me.user.email = form.cleaned_data['email']
			me.location = form.cleaned_data['location']
			me.occupation = form.cleaned_data['occupation']
			me.strengths = form.cleaned_data['strengths']
			me.want_support = form.cleaned_data['want_support']
			me.about_me = form.cleaned_data['about_me']
			me.who_can_view = form.cleaned_data['who_can_view_profile']
			me.i_am_a_health_professional = form.cleaned_data['i_am_a_health_professional']
			me.i_accept_terms_and_conditions = form.cleaned_data['i_accept_terms_and_conditions']
			
			hp_f = HealthProfessional.objects.filter(member=me)
			if (me.i_am_a_health_professional == False and len(hp_f) > 0):
				me.hp_confirmed = False
				hp_f[0].delete()
			elif(me.i_am_a_health_professional == True and len(hp_f) > 0):
				hp_f[0].job_field = form.cleaned_data['job_field']
				hp_f[0].job_title = form.cleaned_data['job_title']
				hp_f[0].credentials = form.cleaned_data['credentials']
				hp_f[0].save()
				
			me.save()
			me.user.save()
			me_goal.save()
			message = "Profile saved."

			nexturl = '/membership/edit_profile/'
			if(request.GET.get('next', False)):
				nexturl = request.GET.get('next')
				return HttpResponseRedirect(nexturl)

	else:
		jf = ""
		jt = ""
		cr = ""
		hp_f = HealthProfessional.objects.filter(member=me)
		if (me.i_am_a_health_professional == True and len(hp_f) > 0):
			jf = hp_f[0].job_field
			jt = hp_f[0].job_title
			cr = hp_f[0].credentials
			
		form = EditProfile(initial={
		'email' : request.user.email,
		'location' : me.location,
		'occupation' : me.occupation,
		'strengths' : me.strengths,
		'want_support' : me.want_support,
		'about_me' : me.about_me,
		'i_am_a_health_professional' : me.i_am_a_health_professional,
		'who_can_view_progress' : me_goal.who_can_view,
		'job_field' : jf,
		'job_title' : jt,
		'credentials' : cr,
		'i_accept_terms_and_conditions' : me.i_accept_terms_and_conditions
		})
	
	
	return render_to_response('membership/edit_profile.html', {
	'me': me,
	'message' : message,
	'form': form,
	}, context_instance=RequestContext(request))

	