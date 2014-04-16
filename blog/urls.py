from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

#from registration.views import activate
#from registration.views import register

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('blog.views',
	# Example:
	# (r'^let_site/', include('let_site.foo.urls')),

	# Uncomment the admin/doc line below and add 'django.contrib.admindocs'
	# to INSTALLED_APPS to enable admin documentation:
	# (r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	# (r'^admin/', include(admin.site.urls)),
	(r'^write/$', 'write'),
	(r'^browse/$', 'browse'),
	(r'^browse/(?P<member_id>\d+)/$', 'browse'),
	(r'^browse/(?P<member_id>\d+)/(?P<entry_id>\d+)/$', 'browse'),
	
	(r'^comment/(?P<entry_id>\w+)/$', 'comment'),
#	(r'^aboutus/$', 'aboutus'),
#	(r'^nutrition/$', 'nutrition'),
#	(r'^exercise/$', 'exercise'),
#	(r'^hp/$', 'hp'),

)
