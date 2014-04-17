from utils import profile_required, hp_profile_required, tnc_required, goal_required, dictsafe
from datetime import datetime, time, timedelta, date
from django.conf import settings
from django.core.mail import send_mail


from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from message.forms import ShoutForm, MessageForm
from message.models import Shout, Message
from membership.models import Member, HealthProfessional, Follow

@login_required
@profile_required
@hp_profile_required
@tnc_required
@goal_required
def browse(request, message_id=None):
	me = Member.objects.get(user=request.user)
	messages_to_me = []
	message=""
	msg = []
	if (message_id):
		try:
			msg = Message.objects.get(id=message_id)		
		except:
			message = "This message does not exist, or it was not written to you."
			return render_to_response('message/browse.html', {
			'message': message,
			}, context_instance=RequestContext(request))	
			
		if (request.method == 'GET' and request.GET.get('remove')):
			msg.delete()
			return HttpResponseRedirect("/message/browse/")			
		else:		
			msg.read_date = datetime.now()
			msg.save()
			return render_to_response('message/browse.html', {
			'msg': msg,
			'message_id': message_id,
			}, context_instance=RequestContext(request))
		

	messages_to_me = me.to_list.all().order_by("send_date").reverse()
	
	
	return render_to_response('message/browse.html', {
	'messages_to_me': messages_to_me,
	}, context_instance=RequestContext(request))

@login_required
@profile_required
@hp_profile_required
@tnc_required
@goal_required
def write(request, msg_id=None, mem_id=None):
	me = Member.objects.get(user=request.user)
	dbmessage=""
	if request.method == 'POST':
		form = MessageForm(request.POST)

		if form.is_valid():
			msg = form.save(commit=False)
			msg.from_member = me
			msg.save()
			send_mail('Find Your Fitness', 'Find Your Fitness: %s has sent you a message. \n"%s"\n\n  Click here to read it:  %s/message/browse/%s/ \n\n(please do not reply to this link)\n - Find Your Fitness'%(msg.from_member.user.username, msg.title, settings.ROOT_SITE_URL, msg.id), 'donotreply', ['%s'%(msg.to_member.user.email)], fail_silently=True)

			message = "Message sent."
			return render_to_response('public_site/home.html', {
			'message': message,
			'dbmessage': dbmessage,
			}, context_instance=RequestContext(request))
	else:
		if (msg_id and mem_id):
			msg_reply = Message.objects.get(id=msg_id)
			mem_reply = Member.objects.get(id=mem_id)
			form = MessageForm(initial={'title':"RE:%s"%(msg_reply.title), 'to_member':mem_reply.user})
		elif (mem_id):
			mem_reply = Member.objects.get(id=mem_id)
			form = MessageForm(initial={'to_member':mem_reply.user})
		else:
			form = MessageForm()
	
	
	return render_to_response('message/write.html', {
	'form': form,
	}, context_instance=RequestContext(request))

@login_required
@profile_required
@hp_profile_required
@tnc_required
@goal_required
def shoutout(request):
	me = Member.objects.get(user=request.user)
	dbmessage = ""
	if request.method == 'POST':
		form = ShoutForm(request.POST)

		if form.is_valid(): 
			t = form.cleaned_data['text']
			shout = Shout.objects.create(text=t, member=me)
			shout.save()
	
			return HttpResponseRedirect('/membership/home/')
		#dbmessage += "%s - %s<br />"%("form not valid!", form.shout_text.error)
	else:
		form = ShoutForm()	
	
	
	return render_to_response('message/shout.html', {
	'form': form,
	'dbmessage': dbmessage,
	}, context_instance=RequestContext(request))


def get_shouts(request):
	max_shouts = 20
	all_shouts = Shout.objects.all().order_by('date').reverse()[:20]
	shout_list = []
	shout_num = len(all_shouts)
	
	for r in range(shout_num):
		shout_dict = {}
		shout_dict['text'] = "%s"%str(all_shouts[r].text).encode('ascii')
		shout_dict['user_id'] = "%s"%str(all_shouts[r].member.user.id).encode('ascii')
		shout_dict['name'] = "%s"%str(all_shouts[r].member.user.username).encode('ascii')			
		shout_dict['conf_hp'] = "%s"%str(all_shouts[r].member.hp_confirmed).encode('ascii')
		shout_list.append(shout_dict)

	"""
	if (shout_num <= max_shouts):
		for r in range(shout_num):
			i = shout_num-r-1
			shout_dict = {}
			shout_dict['text'] = "%s"%str(all_shouts[i].text).encode('ascii')
			shout_dict['member_id'] = "%s"%str(all_shouts[i].member.id).encode('ascii')
			shout_dict['name'] = "%s"%str(all_shouts[i].member.user.username).encode('ascii')			
			shout_dict['conf_hp'] = "%s"%str(all_shouts[i].member.hp_confirmed).encode('ascii')
			shout_list.append(shout_dict)
	else:
		for r in range(max_shouts):
			i = shout_num-r-1
			shout_dict = {}
			shout_dict['text'] = "%s"%str(all_shouts[i].text).encode('ascii')
			shout_dict['member_id'] = "%s"%str(all_shouts[i].member.id).encode('ascii')
			shout_dict['name'] = "%s"%str(all_shouts[i].member.user.username).encode('ascii')			
			shout_dict['conf_hp'] = "%s"%str(all_shouts[i].member.hp_confirmed).encode('ascii')
			shout_list.append(shout_dict)
	
	"""
	"""
	shout_dict = {}
	shout_num = len(all_shouts)
	if (shout_num < 5):
		for r in range(shout_num):
			i = shout_num-r-1
			shout_dict[i] = {}
			shout_dict[i]['text'] = all_shouts[i].text
			shout_dict[i]['member_id'] = all_shouts[i].member.id
			shout_dict[i]['name'] = all_shouts[i].member.user.username				
			shout_dict[i]['conf_hp'] = all_shouts[i].member.hp_confirmed
	else:
		for r in range(4):
			i = shout_num-r-1
			shout_dict[i] = {}
			shout_dict[i]['text'] = all_shouts[i].text
			shout_dict[i]['member_id'] = all_shouts[i].member.id
			shout_dict[i]['name'] = all_shouts[i].member.user.username				
			shout_dict[i]['conf_hp'] = all_shouts[i].member.hp_confirmed
	"""
	this_user = request.user.username
	#shoutDictSafe = dictsafe(shout_dict)
	shoutDictSafe = "%s"%shout_list
	
	return HttpResponse("shoutCallback("+shoutDictSafe+",'"+this_user+"')", mimetype="text/javascript")
	