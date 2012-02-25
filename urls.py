from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # public
    url(r'^elastic/node/$', 'conductor.views.node_landing', name='node-landing'),
    
    # api
    url(r'^elastic/node/announce/$', 'conductor.views.node_announce', name='node-announce'),
    url(r'^elastic/node/getwork/$', 'conductor.views.node_getwork', name='node-getwork'),
    url(r'^elastic/node/emit/$', 'conductor.views.node_emit', name='node-emit'),
    
    # other
    url(r'^admin/', include(admin.site.urls)),
)
