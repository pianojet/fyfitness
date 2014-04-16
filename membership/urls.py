from django.conf.urls import patterns, include, url
#from django.views.generic.simple import direct_to_template

#from registration.views import activate
#from registration.views import register

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('membership.views',
	# Example:
	# (r'^let_site/', include('let_site.foo.urls')),

	# Uncomment the admin/doc line below and add 'django.contrib.admindocs'
	# to INSTALLED_APPS to enable admin documentation:
	# (r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	# (r'^admin/', include(admin.site.urls)),
	url(r'^home/$', 'membership_home'),
	url(r'^post_num/$', 'return_post_num'),	
	url(r'^create_profile/$', 'create_profile'),
	url(r'^create_hp_profile/$', 'create_hp_profile'),
	url(r'^show_profile/$', 'show_profile'),
	url(r'^show_profile/(?P<user_id>\d+)/$', 'show_profile'),	
	url(r'^edit_profile/$', 'edit_profile'),
	url(r'^accept_tnc/$', 'tnc'),
	url(r'^update_progress/$', 'update_progress'),
	url(r'^update_progress/(?P<goal_id>\d+)/$', 'update_progress'),
	url(r'^create_goal/$', 'create_goal'),	
	url(r'^edit_goal/(?P<goal_id>\d+)/$', 'edit_goal'),	
	url(r'^follow/$', 'follow'),
	url(r'^follow/(?P<f_type>\w+)/$', 'follow'),	
	url(r'^follow/(?P<f_type>\w+)/(?P<member_id>\d+)/$', 'follow'),
	
	url(r'^ajax_follow/(?P<member_id>\d+)/$', 'ajax_follow'),
	url(r'^ajax_auth/(?P<member_id>\d+)/$', 'ajax_auth'),	
	url(r'^ajax_unfollow/(?P<member_id>\d+)/$', 'ajax_unfollow'),
	url(r'^ajax_unauth/(?P<member_id>\d+)/$', 'ajax_unauth'),
	url(r'^edit_perm/(?P<object_type>\w+)/(?P<object_id>\d+)/(?P<perm>\w+)/$', 'edit_perm'),
	
#	(r'^aboutus/$', 'aboutus'),
#	(r'^nutrition/$', 'nutrition'),
#	(r'^exercise/$', 'exercise'),
#	(r'^hp/$', 'hp'),

)
