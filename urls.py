from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # public
    url(r'^elastic/node/$', 'conductor.views.node_landing', name='node-landing'),
    
    # api
    url(r'^elastic/node/announce/$', 'conductor.views.node_announce', name='node-announce'),
    url(r'^admin/', include(admin.site.urls)),
)
