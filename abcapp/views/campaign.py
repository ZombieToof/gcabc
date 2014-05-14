from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import DetailView
from django.views.generic import ListView

from abcapp.models import Campaign
from abcapp.models import CampaignMembership


class CampaignList(ListView):

    model = Campaign
    context_object_name = 'campaigns'
    template_name = 'campaigns/index.html'


class CampaignDetailView(DetailView):

    model = Campaign
    context_object_name = 'campaign'
    template_name = 'campaigns/details.html'


class CampaignJoinView(DetailView):

    model = Campaign
    context_object_name = 'campaign'
    template_name = 'campaigns/join.html'

    def get_context_data(self, **context):
        context = super(CampaignJoinView, self).get_context_data(**context)
        campaign = context['campaign']
        user = getattr(self.request, 'user', None)
        context['user'] = user

        try:
            player = user.player
        except (AttributeError, ObjectDoesNotExist):
            context['no_player'] = True
            return context

        membership = CampaignMembership.objects.filter(
            player=player, campaign=campaign).first()

        if membership is not None:
            context['already_joined'] = True
            context['membership'] = membership
            return context

        membership = CampaignMembership.objects.create(
            player=player, campaign=campaign)
        context['membership'] = membership
        context['joined'] = True
        return context
