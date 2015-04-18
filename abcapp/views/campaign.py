from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView

from abcapp.models import Campaign
from abcapp.models import CampaignMembership
from abcapp.models import Player

import logging
logger = logging.getLogger()


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


class CreateCampaignForm(forms.Form):

    army1_name = forms.CharField()
    army1_tag = forms.CharField()
    army1_general = forms.TypedChoiceField(choices=[], coerce=int)

    army2_name = forms.CharField()
    army2_tag = forms.CharField()
    army2_general = forms.TypedChoiceField(choices=[], coerce=int)

    admins = forms.TypedMultipleChoiceField(
        choices=[], coerce=int,
        required=False, widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super(CreateCampaignForm, self).__init__(*args, **kwargs)
        self.set_choices()

    def set_choices(self, ):
        print 'set_choices'
        players = Player.objects.all()

        phpbb_user_choices = [(player.phpbb_user.id,
                               player.phpbb_user.username) for player in
                               players]
        self.fields['army1_general'].choices = phpbb_user_choices
        self.fields['army2_general'].choices = phpbb_user_choices

        player_choices = [(player.id, player.phpbb_user.username) for
                          player in players]
        self.fields['army1_general'].choices = player_choices


class CreateCampaignFormView(TemplateView):

    form_class = CreateCampaignForm
    template_name = 'campaigns/create.html'

    def get_context_data(self, **context):
        user = self.request.user

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            return HttpResponseRedirect('/abc/campaigns')

        context['form'] = form
        return self.render_to_response(context)

    def get(self, request, **kwargs):
        context = self.get_context_data()

        # get the initial data
        context['form'] = self.form_class()
        return self.render_to_response(context)

