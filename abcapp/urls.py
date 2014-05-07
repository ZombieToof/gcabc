from django.conf.urls import patterns, url

from abcapp import views

urlpatterns = patterns(
    '',
    url(r'^campaigns/$', views.campaign.CampaignList.as_view(),
        name='campaigns'),
    url(r'^campaigns/(?P<pk>\d+)/$',
        views.campaign.CampaignDetailView.as_view(),
        name='campaign'),
    url(r'^campaigns/(?P<pk>\d+)/join$',
        views.campaign.CampaignJoinView.as_view(),
        name='campaign-join'),
    url(r'^profile/$',
        views.profile.ProfileView.as_view(),
        name='profile'),
)
