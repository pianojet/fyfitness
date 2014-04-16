from django.db import models
from django.contrib.auth.models import User

from membership.models import Member

class Shout(models.Model):
	member = models.ForeignKey(Member)
	text = models.CharField(max_length=50, blank=False, null=False)
	date = models.DateTimeField(auto_now_add=True)
	
class Message(models.Model):
	from_member = models.ForeignKey(Member, related_name="from_list")
	to_member = models.ForeignKey(Member, related_name="to_list", blank=False, null=False)
	title = models.CharField(max_length=50, blank=False, null=False)	
	text = models.TextField(blank=False, null=False)
	send_date = models.DateTimeField(auto_now_add=True)
	read_date = models.DateTimeField(blank=True, null=True)
	#new_posts = models.ManyToManyField(Entry)