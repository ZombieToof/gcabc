from django.views.generic import TemplateView

from abcapp.models import Campaign


class ProfileView(TemplateView):

    template_name = 'profile/index.html'

    def get_context_data(self, **context):
        context['user'] = getattr(self.request, 'user', None)
        if not context['user']:
            return context

        context['current_campaigns'] = Campaign.current_campaigns()
        context['past_campaigns'] = Campaign.past_campaigns()
        context['upcoming_campaigns'] = Campaign.upcoming_campaigns()
        return context
