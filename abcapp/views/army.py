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
