from django import template
from datetime import datetime, time, timedelta, date
from django.conf import settings

from membership.models import Member, Goal
from blog.models import Entry

import os

register = template.Library()

@register.filter
def get_total_entry_num(id):
	entry_num = 0
	member = Member.objects.filter(id=id)[0]
	entry_num = Entry.objects.filter(member=member).count()
	return entry_num

@register.filter
def get_visible_entry_num(id, user):
	member = Member.objects.filter(id=id)[0]
	entries = Entry.objects.filter(member=member).exclude(who_can_view="Me")
	if len(member.authorized_followers.filter(user=user)) == 0:
		entries = entries.exclude(who_can_view="Restricted")
	return entries.count()

@register.filter
def get_visible_goal_num(id, user):
	member = Member.objects.filter(id=id)[0]
	goals = Goal.objects.filter(member=member).exclude(who_can_view="Me")
	if len(member.authorized_followers.filter(user=user)) == 0:
		goals = goals.exclude(who_can_view="Restricted")
	return goals.count()

@register.filter
def is_following(user1, user2):
	member = Member.objects.filter(user=user1)[0]
 	return len(member.follow.filter(user=user2)) > 0

@register.filter
def has_authorized(user1, user2):
	member = Member.objects.filter(user=user1)[0]
 	return len(member.auth.filter(user=user2)) > 0
