from django.conf.urls import patterns, url

from abcapp import views

urlpatterns = patterns('',
    url(r'^campaigns/$', views.campaign.index, name='campaigns')
)
