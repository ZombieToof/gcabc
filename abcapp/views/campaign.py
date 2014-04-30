from django.views.generic import ListView

from abcapp.models import Campaign


class CampaignList(ListView):

    model = Campaign
    context_object_name = 'campaigns'
    template_name = 'campaigns/index.html'
