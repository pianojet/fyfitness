from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.models import User

from autocomplete.views import autocomplete

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
	
	(r'^admin/', include(admin.site.urls)),
	(r'^$', 'django.views.generic.simple.redirect_to', {'url': '/public_site/'}),
	(r'', include('registration.auth_urls')), 
)

urlpatterns += patterns('',

	(r'^public_site/', include('fyfitness.public_site.urls')),
		
)

urlpatterns += patterns('',

	(r'^accounts/', include('registration.backends.default.urls')),
)


urlpatterns += patterns('',

	(r'^membership/', include('membership.urls')),		
)

urlpatterns += patterns('',

	(r'^blog/', include('blog.urls')),		
)

urlpatterns += patterns('',

	(r'^message/', include('message.urls')),		
)

urlpatterns += patterns('',

	(r'^calendar/', include('calendar.urls')),		
)
