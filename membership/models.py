from datetime import date, timedelta

from django.db import models
from django.contrib.auth.models import User

from blog.models import Entry

GENDER_CHOICES = (
	('M', 'Male'),
	('F', 'Female'),
)

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
	('Other', 'Other'),
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
	('Other', 'Other'),
)

PROGRESS_PERMS = (
	('Me', 'Me'),
	('Restricted', 'Restricted'),
	('Everyone', 'Everyone'),
)	

class Member(models.Model):
	user = models.OneToOneField(User)
	first_name = models.CharField(max_length=50, blank=False, null=False)
	last_name = models.CharField(max_length=50, blank=False, null=False)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=False, null=False)
	location = models.CharField(max_length=50, help_text="Where are you from?", blank=True, null=True)
	member_since = models.DateTimeField(auto_now_add=True)
	occupation = models.CharField(max_length=50, blank=True, null=True)
	strengths = models.TextField(help_text="What are your strengths?", blank=True, null=True)
	want_support = models.TextField(help_text="What specific areas, if any, would you like help with?", blank=True, null=True)
	about_me = models.TextField(help_text="Tell us a little about yourself.", blank=True, null=True)
	who_can_view = models.CharField(help_text="Who will have access to see this profile?", max_length=50, choices=PROGRESS_PERMS, default="Everyone")
	authorized_followers = models.ManyToManyField("self", related_name="auth", symmetrical=False)

	follow = models.ManyToManyField("self", through="Follow", symmetrical=False)	

	i_accept_terms_and_conditions = models.BooleanField()
	i_am_a_health_professional = models.BooleanField()
	hp_confirmed = models.BooleanField(default=False)
	icon = models.URLField(max_length=70, blank=True, null=True)
	
	def get_total_new_post_num(self):
		num = 0
		for f in self.follow.all():
			#get latest entry
			follow_obj = Follow.objects.get(m=self, y=f)
			num += f.entry_set.filter(date_update__gte=follow_obj.blog_last_checked_date).count()
		
		return num

	def get_new_posts(self, member_id):
		posts = []
		u = Member.objects.filter(id=member_id)
		if u[0] in self.follow.all():
			#get latest entry
			follow_obj = Follow.objects.get(m=self, y=u[0])
			f_posts = u[0].entry_set.filter(date_update__gte=follow_obj.blog_last_checked_date)
			for p in f_posts:
				posts.append(p)
		
				
		return posts
		
	def get_all_new_posts(self):
		posts = []
		for f in self.follow.all():
			#get latest entry
			follow_obj = Follow.objects.get(m=self, y=f)
			f_posts = f.entry_set.filter(date_update__gte=follow_obj.blog_last_checked_date)
			for p in f_posts:
				posts.append(p)
		
		
		return posts
	
	
class Follow(models.Model):
	m = models.ForeignKey(Member, related_name="me")
	y = models.ForeignKey(Member, related_name="follow_list")
	
	blog_last_checked_date = models.DateTimeField(auto_now_add=True)
	progress_last_checked_date = models.DateTimeField(auto_now_add=True)
	#new_posts = models.ManyToManyField(Entry)
	
	
class HealthProfessional(models.Model):
	member = models.ForeignKey(Member)
	job_field = models.CharField(max_length=50, choices=FIELD_CHOICES, blank=False, null=False)
	job_title = models.CharField(max_length=50, blank=False, null=False)
	credentials = models.TextField(blank=False, null=False)

class Goal(models.Model):
	member = models.ForeignKey(Member)
	who_can_view = models.CharField(max_length=50, choices=PROGRESS_PERMS, default="Everyone")
	goal_start_date = models.DateField(auto_now_add=True)
	goal_end_date = models.DateField()
 	goal_type = models.CharField(max_length=50, choices=GOAL_TYPE, blank=True, null=True)
 	goal_other_type = models.CharField(max_length=50, blank=True, null=True)
	goal_metric = models.CharField(max_length=50, choices=GOAL_METRIC)	
	goal_unit_number = models.DecimalField(max_digits=5, decimal_places=2)
	starting_unit_number = models.DecimalField(max_digits=5, decimal_places=2)
	goal_unit_type = models.CharField(max_length=50, choices=UNIT, blank=True, null=True)	
	goal_other_unit_type = models.CharField(max_length=50, blank=True, null=True)
	primary_goal = models.BooleanField(default=False)
	
	def can_edit(self):
		if (self.goal_start_date):
			return self.goal_start_date + timedelta(weeks=2) > date.today()
		else:
			return True
	
	def can_change_type(self):
		return self.can_edit() and len(self.progress_set.all()) <= 1
	
	def describe(self, html=True):
		if html:
			return "%s%s: <strong>%s</strong> %s"%("<strong>Primary</strong><br/>" if self.primary_goal else "", self.goal_other_type if self.goal_type == "Other" else self.goal_type, self.goal_unit_number, self.goal_other_unit_type if self.goal_unit_type == "Other" else self.goal_unit_type)
		else:
			return "%s%s: %s %s"%("*" if self.primary_goal else "", self.goal_other_type if self.goal_type == "Other" else self.goal_type, self.goal_unit_number, self.goal_other_unit_type if self.goal_unit_type == "Other" else self.goal_unit_type)

class Progress(models.Model):
	day = models.DateTimeField(auto_now_add=True)
	goal = models.ForeignKey(Goal)
	member = models.ForeignKey(Member)
	current_stat = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)

