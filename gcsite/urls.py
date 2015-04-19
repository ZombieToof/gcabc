from django.views.generic import RedirectView
from django.conf.urls import patterns, include, url
from django.contrib import admin

import abcapp.urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gcsite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', RedirectView.as_view(permanent=False),
        kwargs={'url': '/home'}, name='home'),
    url(r'^djangoadmin/', include(admin.site.urls)),
    url(r'abc/', include(abcapp.urls)),
)
