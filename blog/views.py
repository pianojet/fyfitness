from utils import profile_required, hp_profile_required, tnc_required, goal_required
from datetime import datetime, time, timedelta, date

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from blog.forms import EntryForm, CommentForm
from blog.models import Entry, Comment
from membership.models import Member, HealthProfessional, Follow
from message.models import Message

@login_required
@profile_required
@hp_profile_required
@tnc_required
@goal_required
def write(request):
	me = Member.objects.get(user=request.user)
	dbmessage=""
	if request.method == 'POST':
		form = EntryForm(request.POST)

		if form.is_valid():
			post_text = form.cleaned_data['text']
	
			entry = form.save(commit=False)
			entry.member = me
			entry.save()

			message = "Journal entry saved."
			return render_to_response('public_site/home.html', {
			'message': message,
			'dbmessage': dbmessage,
			}, context_instance=RequestContext(request))
	else:
		form = EntryForm()	
	
	
	return render_to_response('blog/write.html', {
	'form': form,
	}, context_instance=RequestContext(request))

@login_required
@profile_required
@hp_profile_required
@tnc_required
@goal_required
def browse(request, member_id=None, entry_id=None):
	
	member_entries = []
	m = None
	existing_comments = []
	entry = None
	me = Member.objects.get(user=request.user)
	dbmessage = ""
	update_dates = []
	
	#all_my_auth = me.auth.all()
	all_my_foll = me.follow.all()
	
	follow_post_table = "<table id='recent_posts'><tbody>"
	
	#im_following = me.follow.all()
	#for f in im_following:
	#	dbmessage += "%s<br />"%(f)
	#dbmessage += "%s<br />"%(me.get_all_new_posts())
	new_posts = me.get_all_new_posts()
	for p in new_posts:
		post_mem = Member.objects.get(id=p.member_id)
		
		post_mem_name = "<strong class='p_hp'>%s</strong>"%post_mem.user.username if (post_mem.hp_confirmed == True) else "<strong class='p_nohp'>%s</strong>"%post_mem.user.username
		follow_post_table += "<tr><td><a href='/membership/show_profile/%s/'>%s</a></td>"%(p.member_id, post_mem_name)
		follow_post_table += "<td><a href='/blog/browse/%s/%s/'>%s</a></td>"%(p.member_id, p.id, p.date)
		follow_post_table += "<td><a href='/blog/browse/%s/%s/'>%s</a></td></tr>"%(p.member_id, p.id, p.title)
		#dbmessage += follow_post_table
	follow_post_table += "</tbody></table>"
	
	
	all_members = Member.objects.all()
	if member_id != None and entry_id == None:
		m = Member.objects.get(id=member_id)
		all_member_entries = Entry.objects.filter(member=m).order_by('date').reverse()
		#all_member_entries = m.entry_set.all().order_by('date')
		auth_f = m.auth.filter(id=me.id)
		if (len(auth_f) > 0):
			for e in all_member_entries:
				if (e.who_can_view == "Everyone" or e.who_can_view == "Restricted" or e.member == me):
					member_entries.append(e)
					
		else:
			for e in all_member_entries:
				if (e.who_can_view == "Everyone" or e.member == me):
					member_entries.append(e)		
	if entry_id != None:
		m = Member.objects.get(id=member_id)
		m_entry = Entry.objects.get(id=entry_id)
		if ((m.authorized_followers.filter(id=me.id) and m_entry.who_can_view == "Restricted") or m_entry.who_can_view == "Everyone" or m_entry.member == me):
			entry = m_entry
			existing_comments = Comment.objects.filter(entry=entry).order_by('date')
			Follow.objects.filter(y=m, m=me).update(blog_last_checked_date = datetime.now())

	return render_to_response('blog/browse.html', {
	'all_members': all_members, 'all_my_foll' : all_my_foll,
	'follow_post_table' : follow_post_table, 'new_posts': new_posts,
	'dbmessage': dbmessage,
	'member_id': member_id, 'member_entries': member_entries, 'm': m,
	'entry_id': entry_id, 'entry': entry, 'existing_comments': existing_comments,
	}, context_instance=RequestContext(request))
	
@login_required
@profile_required
@hp_profile_required
@tnc_required
@goal_required
def comment(request, entry_id):

	entry = Entry.objects.get(id=entry_id)
	m = entry.member
	existing_comments = Comment.objects.filter(entry=entry).order_by('date')
	this_member = Member.objects.get(user=request.user)
	
	if request.method == 'POST':
		form = CommentForm(request.POST)

		if form.is_valid(): 
			comment = form.save(commit=False)
			comment.entry = Entry.objects.get(id=entry_id)
			comment.from_member = this_member
			comment.save()
			entry.date_update = datetime.now()
			entry.save()
			existing_comments = Comment.objects.filter(entry=entry).order_by('date')			
			message = "Comment entry saved."
			return render_to_response('blog/browse.html', {
			'm': m,
			'message': message,
			'entry_id': entry_id, 'entry': entry, 'existing_comments': existing_comments,
			}, context_instance=RequestContext(request))
	else:
		form = CommentForm()	
	
		
	return render_to_response('blog/browse.html', {
	'form': form,
	'm': m,
	'entry_id': entry_id, 'entry': entry, 'existing_comments': existing_comments,	
	}, context_instance=RequestContext(request))
