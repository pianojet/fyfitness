from django import forms
from django.db import models
from django.contrib.auth.models import User

from autocomplete.widgets import AutoCompleteWidget

from django.forms import ModelForm, TypedChoiceField, ModelChoiceField
from membership.models import Member, HealthProfessional, Progress, Goal
from message.models import Message

FIELD_CHOICES = (
	('Health Administration / Office Support', 'Health Administration / Office Support'),
	('Anesthesiology', 'Anesthesiology'),
	('Chiropractics', 'Chiropractics'),
	('Dental Care', 'Dental Care'),
	('Dietitian / Nutritionist', 'Dietitian / Nutritionist'),
	('Experimental Medicine', 'Experimental Medicine'),
	('Fitness & Exercise', 'Fitness & Exercise'),
	('Geriatrics & Aging', 'Geriatrics & Aging'),
	('Gastroenterology', 'Gastroenterology'),
	('Hospice Care', 'Hospice Care'),
	('Medical Techs / Aides', 'Medical Techs / Aides'),
	('Mental Health', 'Mental Health'),
	('Midwifery', 'Midwifery'),
	('Nursing', 'Nursing'),
	('Pathology', 'Pathology'),
	('Pharmacology & Pharmaceutics', 'Pharmacology & Pharmaceutics'),
	('Public Health', 'Public Health'),
	('Radiation (including Rad. Oncology) / Diagnostic Imaging', 'Radiation (including Rad. Oncology) / Diagnostic Imaging'),
	('Rehabilitative Therapies', 'Rehabilitative Therapies'),
	('Sports Medicine', 'Sports Medicine'),
	('Transplantation', 'Transplantation'),
)

GOAL_TYPE = (
	('Weight', 'Weight'),
	('Body Fat %', 'Body Fat %'),	
	('Measure', (
		('Waist', 'Waist'),
		('Arms', 'Arms'),
		)
	),
	('Exercise Performance', (
		('Bench Press', 'Bench Press'),
		('Squat', 'Squat'),
		('Push Up', 'Push Up'),
		('Sit Up', 'Sit Up'),
		('Pull Up', 'Pull Up'),
		('Running', 'Running'),
		('Swimming', 'Swimming'),
		)
	),
)

GOAL_METRIC = (
	('Percent', 'Percent'),
	('Amount', 'Amount'),
	('Distance', 'Distance'),
	('Time', 'Time'),
)

UNIT = (
	('Inches', 'Inches'),
	('Minutes', 'Minutes'),
	('Pounds', 'Pounds'),
	('Miles', 'Miles'),
	('Laps', 'Laps'),
	('Reps in 1 set', 'Reps in 1 set'),
	('Reps in 1 minute', 'Reps in 1 minute'),
	('%', '%'),
)

PROGRESS_PERMS = (
	('Me', 'Me'),
	('Restricted', 'Restricted'),
	('Everyone', 'Everyone'),
)	


class MemberForm(ModelForm):

#validators?

	class Meta:
		model = Member
		exclude = ['member_since', 'user', 'authorized_followers', 'follow', 'hp_confirmed', 'icon']
		
		
	def clean(self):
		cleaned_data = self.cleaned_data

		return cleaned_data

	

class HealthProfessionalForm(ModelForm):
	class Meta:
		model = HealthProfessional
		exclude = ['member']
		
def is_float(s):
	try:
		float(s)
		return True
	except Exception:
		return False

		
class GoalForm(ModelForm):

#validators?

	class Meta:
		model = Goal
		exclude = ['goal_start_date', 'goal_end_date', 'member']
	
	primary_goal = TypedChoiceField(choices=[(True, "Yes"), (False, "No")], coerce=bool, help_text="You must have a primary goal to use the website, and you can only have 1 primary goal.")
	
	# def clean_primary_goal(self):
	# 	if self.data['primary_goal'] == "0":
	# 		return False
	# 	return True
	
	def clean(self):
		cleaned_data = self.cleaned_data
		if self.instance != None and not self.instance.can_edit():
			msg = "You cannot edit goals which are over 2 weeks old."
			self._errors["__all__"] = self.error_class([msg])
			return cleaned_data
		#cc_myself = cleaned_data.get("cc_myself")
		#subject = cleaned_data.get("subject")
		"""
		GOAL_TYPE = (
			('Weight', 'Weight'),
			('Body Fat %', 'Body Fat %'),			
			('Measure', (
				('Waist', 'Waist'),
				('Arms', 'Arms'),
				)
			),

			('Exercise Performance', (
				('Bench Press', 'Bench Press'),
				('Squat', 'Squat'),
				('Push Up', 'Push Up'),
				('Sit Up', 'Sit Up'),
				('Pull Up', 'Pull Up'),
				('Running', 'Running'),
				('Swimming', 'Swimming'),
				)
			),
		)

		GOAL_METRIC = (
			('Percent', 'Percent'),
			('Amount', 'Amount'),
			('Distance', 'Distance'),
			('Time', 'Time'),
		)

		UNIT = (
			('Inches', 'Inches'),
			('Minutes', 'Minutes'),
			('Pounds', 'Pounds'),
			('Miles', 'Miles'),
			('Laps', 'Laps'),
			('Reps in 1 set', 'Reps in 1 set'),
			('Reps in 1 minute', 'Reps in 1 minute'),
			('%', '%'),
		)
		"""
		T = cleaned_data.get("goal_type")
		O_T = cleaned_data.get("goal_other_type")
		M = cleaned_data.get("goal_metric")
		U = cleaned_data.get("goal_unit_type")
		O_U = cleaned_data.get("goal_other_unit_type")
		N = cleaned_data.get("goal_unit_number")
		S = cleaned_data.get("starting_unit_number")


		"""
		if not((T == "Weight") and (M == "Amount") and (U == "Pounds")) and not((T == "Waist" or T == "Arms") and (M == "Amount") and (U == "Inches")):
		
			#and not((T == "Swimming" or T == "Running") and (((M == "Distance") and (U == "Miles" or U == "Laps")) or ((M == "Time") and (U == "Minutes")))):
			msg = "This combination of Goal Type, Goal Metric, and Unit do not make sense."
			self._errors["goal_type"] = self.error_class([msg])
			self._errors["goal_metric"] = self.error_class([msg])
			self._errors["goal_unit_type"] = self.error_class([msg])
		"""
		if self.instance != None and not self.instance.can_change_type() and self.instance.goal_type != cleaned_data['goal_type']:
			msg = "You can't change the goal type once you've logged progress."
			self._errors["goal_type"] = self.error_class([msg])
		if not(is_float(N)):
			msg = "Invalid number - please use real numbers or decimals."
			self._errors["goal_unit_number"] = self.error_class([msg])
		if not(is_float(S)):
			msg = "Invalid number - please use real numbers or decimals."
			self._errors["starting_unit_number"] = self.error_class([msg])			
		#if <GOAL_TYPE, GOAL_METRIC, and UNIT are not aligned>:
			# make error messages
			#msg = u"This combination of Goal Type, Goal Metric, and Unit do not make sense."
			#self._errors["goal_type"] = self.error_class([msg])
			#self._errors["goal_metric"] = self.error_class([msg])
			#self._errors["goal_unit_type"] = self.error_class([msg])
			#self._errors["goal_unit_number"] = self.error_class([msg])


		# Always return the full collection of cleaned data.
		return cleaned_data
		
class ProgressForm(forms.Form):
	goal_to_update = forms.ChoiceField()
	current_stat = forms.DecimalField(max_digits=5, decimal_places=2)
	default_data = {'who_can_view': 'Everyone'}

class MessageForm(forms.ModelForm):
	class Meta:
		model = Message

	user = ModelChoiceField('user')	
    
class AcUserForm1(forms.Form):
	# an existent user
	an_existent_user1 = ModelChoiceField('user', label="Username")

	# an existent username
	#an_existent_username = forms.CharField(widget=AutoCompleteWidget('name'))
	# an username, either existent or not
	#an_username = forms.CharField(widget=AutoCompleteWidget('name', force_selection=False))

class AcUserForm2(forms.Form):
	# an existent user
	an_existent_user2 = ModelChoiceField('user', label="Username")

	# an existent username
	#an_existent_username = forms.CharField(widget=AutoCompleteWidget('name'))
	# an username, either existent or not
	#an_username = forms.CharField(widget=AutoCompleteWidget('name', force_selection=False))

class EditProfile(forms.Form):
	email = forms.EmailField(required=True)
	location = forms.CharField(max_length=50, required=False)
	occupation = forms.CharField(max_length=50, required=False)
	strengths = forms.CharField(widget=forms.Textarea(), required=False)
	want_support = forms.CharField(widget=forms.Textarea(), required=False)
	about_me = forms.CharField(widget=forms.Textarea(), required=False)
	who_can_view_profile = forms.CharField(label="Who can view profile?", max_length=50, widget=forms.Select(choices=PROGRESS_PERMS))
	i_am_a_health_professional = forms.BooleanField(required=False)
	i_accept_terms_and_conditions = forms.BooleanField(required=False)

	job_field = forms.CharField(max_length=50, widget=forms.Select(choices=FIELD_CHOICES),required=False)
	job_title = forms.CharField(max_length=50,required=False)
	credentials = forms.CharField(widget=forms.Textarea,required=False)


class tncForm(forms.Form):
	# an existent user
	i_accept_terms_and_conditions = forms.BooleanField(required=False)
