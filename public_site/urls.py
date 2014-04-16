from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('public_site.views',
    # Example:
    # (r'^let_site/', include('let_site.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
        (r'^$', 'home'),
	(r'^news/$', 'news'),
	(r'^aboutus/$', 'aboutus'),
	(r'^nutrition/$', 'nutrition'),
	(r'^exercise/$', 'exercise'),
	(r'^hp/$', 'hp'),
	(r'^faq/$', 'faq'),
	
#        (r'^what_is_expressive_therapy/$', 'whatis'),
#        (r'^services/$', 'services'),
#        (r'^benefit/$', 'benefit'),
#        (r'^meet/$', 'meet'),
#        (r'^links/$', 'links'),
#        (r'^faq/$', 'faq'),
#        (r'^contact/$', 'contact'),
#        (r'^testimonials/$', 'testimonials'),

)
