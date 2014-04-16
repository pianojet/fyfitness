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
def browse(request, member_id=None):
	message = ""

	return render_to_response('calendar/browse.html', {
	'message': message,
	}, context_instance=RequestContext(request))
	
