from django.conf.urls import patterns, url

from abcapp import views

urlpatterns = patterns(
    '',
    url(r'^campaigns/$', views.campaign.CampaignList.as_view(),
        name='campaigns'),
    url(r'^campaigns/(?P<pk>\d+)/$',
        views.campaign.CampaignDetailView.as_view(),
        name='campaign'),
)
