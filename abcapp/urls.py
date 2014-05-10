from django.conf.urls import patterns, url

from abcapp import views

urlpatterns = patterns(
    '',
    url(r'^campaigns/$', views.campaign.CampaignList.as_view(),
        name='abcapp.campaigns'),
    url(r'^campaigns/(?P<pk>\d+)/$',
        views.campaign.CampaignDetailView.as_view(),
        name='abcapp.campaign'),
    url(r'^campaigns/(?P<pk>\d+)/join$',
        views.campaign.CampaignJoinView.as_view(),
        name='abcapp.campaign.join'),
    url(r'^army/$',
        views.army.ArmyListView.as_view(),
        name='abcapp.army'),
    url(r'^profile/$',
        views.profile.ProfileView.as_view(),
        name='profile'),
)
