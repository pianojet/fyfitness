from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

#from registration.views import activate
#from registration.views import register

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('message.views',
	# Example:
	# (r'^let_site/', include('let_site.foo.urls')),

	# Uncomment the admin/doc line below and add 'django.contrib.admindocs'
	# to INSTALLED_APPS to enable admin documentation:
	# (r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	# (r'^admin/', include(admin.site.urls)),
	(r'^shoutout/$', 'shoutout'),
	(r'^get_shouts/$', 'get_shouts'),
	(r'^write/$', 'write'),
	(r'^write/(?P<mem_id>\w+)/$', 'write'),	
	(r'^write/(?P<msg_id>\w+)/(?P<mem_id>\w+)/$', 'write'),	
	(r'^browse/$', 'browse'),
	(r'^browse/(?P<message_id>\d+)/$', 'browse'),
#	(r'^aboutus/$', 'aboutus'),
#	(r'^nutrition/$', 'nutrition'),
#	(r'^exercise/$', 'exercise'),
#	(r'^hp/$', 'hp'),

)
