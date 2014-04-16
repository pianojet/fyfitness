from utils import words_avoided
from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, ModelChoiceField

from autocomplete.widgets import AutoCompleteWidget
#from autocomplete.fields import ModelChoiceField

from membership.models import Member

from message.models import Shout, Message

class ShoutForm(forms.Form):
	text = forms.CharField(max_length=50)
	def clean_text(self):
		t = self.cleaned_data.get('text', '')
		for w in words_avoided:
			w_len = len(w)
			t_rep = ""
			if (t.find(w) != -1):
				for t_rep_count in range(w_len):
					t_rep += "X"
				t = str(t).replace(w,t_rep)
		return t
		
		
class MessageForm(ModelForm):
	class Meta:
		model = Message
		exclude = ['from_member', 'send_date', 'read_date']
		
	to_member = ModelChoiceField('user', label="To:")

	def clean_to_member(self):
		user = self.cleaned_data.get('to_member', '')
		member = []
		member = Member.objects.filter(user=user)
		if member:
			if (len(member) == 1):
				return member[0]
			else:
				raise forms.ValidationError("This person has not completed registration.")
		else:
			raise forms.ValidationError("This person has not completed registration.")

		
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
