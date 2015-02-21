from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:

    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'gojira.general.views.home_view', name='home'),
    url(r'^home/$', 'gojira.general.views.home_view', name='home'),
    url(r'^admin/', include(admin.site.urls)),
)
