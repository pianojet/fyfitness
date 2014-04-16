from django import template
from datetime import datetime, time, timedelta, date
from django.conf import settings

from membership.models import Member
from blog.models import Entry

import os

register = template.Library()

@register.filter
def user_widget(member_id, arg):

	me_f = Member.objects.filter(user=arg)
	member = Member.objects.filter(id=member_id)[0]
	hpclass = "p_nothp" if not(member.hp_confirmed) else "p_hp"
	if len(me_f) > 0:
	#	<a href="/membership/show_profile/{{m.user.id}}/"><strong class="{% ifequal m.hp_confirmed 1 %}p_hp{% else %}p_nothp{% endifequal %}">{{ m.user.username }}</strong></a>

		all_my_auth = me_f[0].auth.all()
		all_my_foll = me_f[0].follow.all()

		if (member in all_my_auth):
			auth_image = "auth_sub.png"
			auth_alt = "Un-Authorize this member"
			auth_onclick = "sub"
		else:
			auth_image = "auth_add.png"
			auth_alt = "Authorize this member"
			auth_onclick = "add"
			
		if (member in all_my_foll):
			follow_image = "follow_sub.png"
			follow_alt = "Un-Follow this member"
			follow_onclick = "sub"
		else:
			follow_image = "follow_add.png"
			follow_alt = "Follow this member"
			follow_onclick = "add"
			

		html_string = "<span class='user_links'>"
		html_string += "<a href='/membership/show_profile/%s/' title='View Profile'><strong class='%s'>%s</strong></a>"%(member.user.id, hpclass, member.user.username)
		html_string += "<a href='/message/write/%s/' title='Send Message'><img alt='Profile' src='../images/message_icon.png' /></a>"%(member_id)
		html_string += "<a href='/blog/browse/%s/' title='View Journal Entries'><img alt='journal' src='../images/journal_icon.png' /></a>"%(member_id)

		html_string += "<img class='auth_%s_%s' title='%s' alt='%s' src='../images/%s' />"%(auth_onclick, member_id, auth_alt, auth_alt, auth_image)
		html_string += "<img class='foll_%s_%s' title='%s' alt='%s' src='../images/%s' />"%(follow_onclick, member_id, follow_alt, follow_alt, follow_image)		
		
		html_string += "</span>"
	else:

		html_string = "<span class='user_links'>"
		html_string += "<a href='/membership/show_profile/%s/'><strong class='%s'>%s</strong></a>"%(member.user.id, hpclass, member.user.username)
		#html_string += "<a href='/message/write/%s' title='Send Message'><img alt='Profile' src='../images/message_icon.png' /></a>"%(member.id)
		#html_string += "<a href='/blog/browse/%s/' title='View Journal Entries'><img alt='journal' src='../images/journal_icon.png' /></a>"%(member.id)
		html_string += "</span>"


	return html_string
