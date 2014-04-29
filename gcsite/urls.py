from django.conf.urls import patterns, include, url
from django.contrib import admin

import abcapp.urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gcsite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'abc/', include(abcapp.urls)),
)
