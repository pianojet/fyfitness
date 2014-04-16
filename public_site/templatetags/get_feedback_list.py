from django import template
from datetime import datetime, time, timedelta, date
from django.conf import settings

from blog.models import Entry

import os

register = template.Library()

@register.filter
def get_feedback_list(dummy):
	feedback_entry_list = []
	time_span = timedelta(days=8)
	time_ago = datetime.now() - time_span	
	feedback_entry_list = Entry.objects.filter(date_update__gte=time_ago, do_you_want_feedback=True).order_by('date').reverse()
	return feedback_entry_list
