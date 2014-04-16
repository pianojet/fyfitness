from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

from blog.models import Entry
from blog.models import Comment

class EntryForm(ModelForm):

#validators?

	class Meta:
		model = Entry
		exclude = ['date', 'member', 'date_update']
		
		
	def clean(self):
		cleaned_data = self.cleaned_data
		#cc_myself = cleaned_data.get("cc_myself")
		#subject = cleaned_data.get("subject")

		#if <stuffs not right>:
			# make error messages
			#msg = u"error"
			#self._errors[""] = self.error_class([msg])



		# Always return the full collection of cleaned data.
		return cleaned_data

		

class CommentForm(ModelForm):
	class Meta:
		model = Comment
		exclude = ['entry', 'date', 'from_member']