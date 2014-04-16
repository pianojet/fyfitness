#from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.models import User
from django.conf.urls import patterns, include, url

from autocomplete.views import autocomplete
from django.views.generic import RedirectView

admin.autodiscover()

autocomplete.register(
    id = 'user',
    queryset = User.objects.all(),
    fields = ['username']
    #limit = 5,
)

"""
autocomplete.register(
    id = 'name',
    queryset = User.objects.all(),
    fields = ['username']
    #limit = 5,
    #key = 'username'.encode('ascii'),
    #label = 'username'.encode('ascii'),
)
"""

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	# Example:
	# (r'^fyfitness/', include('fyfitness.foo.urls')),

	# Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
	# to INSTALLED_APPS to enable admin documentation:
	# (r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	url(r'^autocomplete/(\w+)/$', autocomplete, name='autocomplete'),
	
	url(r'^admin/', include(admin.site.urls)),
	url(r'^$', RedirectView.as_view(url='/public_site')),
	url(r'', include('registration.auth_urls')), 
)

urlpatterns += patterns('',

	url(r'^public_site/', include('public_site.urls')),
		
)

urlpatterns += patterns('',

	url(r'^accounts/', include('registration.backends.default.urls')),
)


urlpatterns += patterns('',

	url(r'^membership/', include('membership.urls')),		
)

urlpatterns += patterns('',

	url(r'^blog/', include('blog.urls')),		
)

urlpatterns += patterns('',

	url(r'^message/', include('message.urls')),		
)

urlpatterns += patterns('',

	url(r'^calendar/', include('calendar.urls')),		
)
