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
    url(r'^campaigns/(?P<pk>\d+)/army/$',
        views.army.CampaignArmyListView.as_view(),
        name='abcapp.campaign.army'),
    url(r'^campaigns/(?P<pk>\d+)/army/(?P<army_id>\d+)$',
        views.army.CampaignArmyDetailView.as_view(),
        name='abcapp.campaign.army.details'),
    url(r'^campaigns/(?P<pk>\d+)/army/(?P<army_id>\d+)/'
        r'player/(?P<membership_id>\d+)/edit$',
        views.army.EditArmyMemberFormView.as_view(),
        name='abcapp.campaign.army.member.edit'),
    url(r'^campaigns/(?P<pk>\d+)/army/(?P<army_id>\d+)/'
        r'player/(?P<membership_id>\d+)/dismiss$',
        views.army.DismissArmyMemberFormView.as_view(),
        name='abcapp.campaign.army.member.dismiss'),
    url(r'^army/$',
        views.army.ArmyListView.as_view(),
        name='abcapp.army'),
    url(r'^profile/$',
        views.profile.ProfileView.as_view(),
        name='profile'),
)
