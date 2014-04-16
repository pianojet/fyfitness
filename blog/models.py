from django.db import models
from django.contrib.auth.models import User

#from membership.models import Member, HealthProfessional

PROGRESS_PERMS = (
	('Me', 'Me'),
	('Restricted', 'Restricted'),
	('Everyone', 'Everyone'),
)	


class Entry(models.Model):
	member = models.ForeignKey('membership.Member')
	title = models.CharField(max_length=30, blank=False, null=False)
	date = models.DateTimeField(auto_now_add=True)
	text = models.TextField(blank=False, null=False)
	who_can_view = models.CharField(max_length=50, choices=PROGRESS_PERMS, default="Everyone")
	do_you_want_feedback = models.BooleanField(help_text="Would you like feedback?")
	date_update = models.DateTimeField(auto_now_add=True)
	
	

class Comment(models.Model):
	entry = models.ForeignKey(Entry)
	from_member = models.ForeignKey('membership.Member')
	date = models.DateTimeField(auto_now_add=True)
	text = models.TextField(blank=False, null=False)
	