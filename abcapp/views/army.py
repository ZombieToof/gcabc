from django.views.generic import DetailView
from django.views.generic import ListView

from abcapp.models import Army


class ArmyListView(ListView):

    model = Army
    context_object_name = 'armies'
    template_name = 'army/index.html'

    def get_queryset(self):
        return Army.objects.order_by('campaign__start')
