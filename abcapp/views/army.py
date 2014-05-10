from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.views.generic import ListView

from abcapp.models import Army
from abcapp.models import Campaign


class ArmyListView(ListView):

    model = Army
    context_object_name = 'armies'
    template_name = 'army/index.html'

    def get_queryset(self):
        return Army.objects.order_by('campaign__start')


class CampaignArmyListView(ArmyListView):

    template_name = 'army/campaign_index.html'

    def get_context_data(self, **context):
        q = super(CampaignArmyListView, self).get_queryset()
        campaign = get_object_or_404(Campaign, id=self.kwargs['pk'])
        armies = q.filter(campaign=campaign).all()
        context['armies'] = armies
        context['campaign'] = campaign
        return context


class CampaignArmyDetailView(DetailView):

    model = Campaign
    context_object_name = 'campaign'
    template_name = 'army/details.html'

    def get_context_data(self, **context):
        context = super(CampaignArmyDetailView,
                        self).get_context_data(**context)
        campaign = context['campaign']
        army = get_object_or_404(Army, id=self.kwargs['army_id'],
                                 campaign=campaign)
        context['army'] = army
        context['players'] = army.players.order_by('title').all()
        context['divisions'] = army.divisions
        ## # player
        ## user = getattr(self.request, 'user', None)
        ## context['user'] = user
        ## try:
        ##     player = user.player
        ## except (AttributeError, ObjectDoesNotExist):
        ##     context['no_player'] = True
        ##     return context

        ## participation = CampaignParticipation.objects.filter(
        ##     player=player, campaign=campaign).first()

        ## if participation is not None:
        ##     context['already_joined'] = True
        ##     context['participation'] = participation
        ##     return context

        return context
