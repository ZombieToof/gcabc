from django import forms
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView

from abcapp.models import Army
from abcapp.models import Campaign
from abcapp.models import CampaignParticipation
from abcapp.models import Division
from abcapp.models import Medal
from abcapp.models import Rank


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
        context['participations'] = army.participations.all()
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


class EditArmyMemberForm(forms.Form):

    rank = forms.TypedChoiceField(choices=[], coerce=int, required=False)
    division = forms.TypedChoiceField(choices=[], coerce=int, required=False)
    medals = forms.TypedMultipleChoiceField(
        choices=[], coerce=int,
        required=False, widget=forms.CheckboxSelectMultiple)
    notes = forms.CharField(required=False,
                            widget=forms.Textarea)

    def __init__(self, participation, *args, **kwargs):
        super(EditArmyMemberForm, self).__init__(*args, **kwargs)
        self.set_choices(participation)

    def set_choices(self, participation):
        army = participation.army

        rank_choices = [(rank.id, rank.title) for rank in army.sorted_ranks()]
        self.fields['rank'].choices = rank_choices

        division_choices = [(division.id, division.title) for division
                            in army.divisions.all()]
        self.fields['division'].choices = division_choices

        medal_choices = [(medal.id, medal.title) for medal in
                         army.sorted_medals()]
        self.fields['medals'].choices = medal_choices


class EditArmyMemberFormView(TemplateView):

    form_class = EditArmyMemberForm
    template_name = 'army/edit_army_member.html'

    def get_context_data(self, **context):
        army = get_object_or_404(Army, id=self.kwargs['army_id'])
        participation = get_object_or_404(CampaignParticipation,
                                          id=self.kwargs['participation_id'],
                                          army=army)
        context['army'] = army
        context['participation'] = participation
        user = self.request.user
        if user.is_anonymous():
            raise PermissionDenied('Nope')  # FIXME: Template with reason
        if not army.is_officer(user.player):
            raise PermissionDenied('Nope')  # FIXME: Template with reason
        # FIXME: more permission checks?

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        form = EditArmyMemberForm(context['participation'],
                                  request.POST)

        if form.is_valid():
            data = form.cleaned_data
            participation = context['participation']
            participation.division = Division.objects.filter(
                id=data['division']).first()
            participation.rank = Rank.objects.filter(
                id=data['rank']).first()
            medals = Medal.objects.filter(pk__in=data['medals'])
            participation.medals = medals
            participation.notes = data['notes']
            participation.save()

            messages.add_message(request, messages.SUCCESS,
                                 "Saved. Didn't think we would, did you?")

            return HttpResponseRedirect(context['army'].details_url)

        context['form'] = form
        return self.render_to_response(context)

    def get(self, request, **kwargs):
        context = self.get_context_data()

        # get the initial data
        participation = context['participation']
        rank = participation.current_rank()
        rank_id = rank.id if rank else None
        division = participation.division
        division_id = division.id if division else None
        medal_ids = [medal.id for medal in participation.medals.all()]
        
        initial_data = {'rank': rank_id,
                        'division': division_id,
                        'medals': medal_ids,
                        'notes': participation.notes}
        context['form'] = EditArmyMemberForm(participation,
                                             initial=initial_data)
        return self.render_to_response(context)
