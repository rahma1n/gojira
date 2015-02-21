from django.conf.urls import patterns, url


__author__ = 'nadimrahman'


urlpatterns = patterns('gojira.general.views',
    # Examples:
    # url(r'^$', 'gojira.views.home', name='home'),

    url(r'^home/$', 'home-view', name='home'),

)

