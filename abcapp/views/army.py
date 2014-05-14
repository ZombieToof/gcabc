from django import forms
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView

from abcapp.models import Army
from abcapp.models import Campaign
from abcapp.models import CampaignMembership
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
        context['memberships'] = army.memberships.all()
        context['divisions'] = army.divisions
        ## # player
        ## user = getattr(self.request, 'user', None)
        ## context['user'] = user
        ## try:
        ##     player = user.player
        ## except (AttributeError, ObjectDoesNotExist):
        ##     context['no_player'] = True
        ##     return context

        ## membership = CampaignMembership.objects.filter(
        ##     player=player, campaign=campaign).first()

        ## if membership is not None:
        ##     context['already_joined'] = True
        ##     context['membership'] = membership
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

    def __init__(self, membership, *args, **kwargs):
        super(EditArmyMemberForm, self).__init__(*args, **kwargs)
        self.set_choices(membership)

    def set_choices(self, membership):
        army = membership.army

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
        membership = get_object_or_404(CampaignMembership,
                                          id=self.kwargs['membership_id'],
                                          army=army)
        context['army'] = army
        context['membership'] = membership
        user = self.request.user
        if user.is_anonymous():
            raise PermissionDenied('Nope')  # FIXME: Template with reason
        if not army.is_officer(user.player):
            raise PermissionDenied('Nope')  # FIXME: Template with reason
        # FIXME: more permission checks?

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        form = EditArmyMemberForm(context['membership'],
                                  request.POST)
        if form.is_valid():
            data = form.cleaned_data
            membership = context['membership']
            membership.division = Division.objects.filter(
                id=data['division']).first()
            membership.rank = Rank.objects.filter(
                id=data['rank']).first()
            medals = Medal.objects.filter(pk__in=data['medals'])
            membership.medals = medals
            membership.notes = data['notes']
            membership.save()

            messages.add_message(request, messages.SUCCESS,
                                 "Saved. Didn't think we would, did you?")

            return HttpResponseRedirect(context['army'].details_url)

        context['form'] = form
        return self.render_to_response(context)

    def get(self, request, **kwargs):
        context = self.get_context_data()

        # get the initial data
        membership = context['membership']
        rank = membership.current_rank()
        rank_id = rank.id if rank else None
        division = membership.division
        division_id = division.id if division else None
        medal_ids = [medal.id for medal in membership.medals.all()]
        
        initial_data = {'rank': rank_id,
                        'division': division_id,
                        'medals': medal_ids,
                        'notes': membership.notes}
        context['form'] = EditArmyMemberForm(membership,
                                             initial=initial_data)
        return self.render_to_response(context)


class DismissArmyMemberForm(forms.Form):

    dismiss = forms.BooleanField(label=u'Yes, dismiss the player',
                                 required=True)


class DismissArmyMemberFormView(TemplateView):

    template_name = 'army/dismiss_army_member.html'

    def get_context_data(self, **context):
        army = get_object_or_404(Army, id=self.kwargs['army_id'])
        membership = get_object_or_404(CampaignMembership,
                                          id=self.kwargs['membership_id'],
                                          army=army)
        context['army'] = army
        context['membership'] = membership
        user = self.request.user
        if user.is_anonymous():
            raise PermissionDenied('Nope')  # FIXME: Template with reason
        if not army.is_officer(user.player):
            raise PermissionDenied('Nope')  # FIXME: Template with reason
        # FIXME: more permission checks?
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        form = DismissArmyMemberForm(request.POST)
        redirect_to_listing = HttpResponseRedirect(context['army'].details_url)

        if 'cancel' in form.data:
            return redirect_to_listing

        if form.is_valid():
            data = form.cleaned_data
            if data['dismiss']:
                membership = context['membership']
                try:
                    player = request.user.player
                    username = player.title
                except ObjectDoesNotExist:
                    username = request.user.username
                notes = membership.notes
                notes_addition = '\n\nDismissed from %s by %s on %s' % (
                    membership.army.title, username,
                    timezone.now().isoformat())
                membership.notes = notes + notes_addition
                membership.army = None
                membership.division = None
                membership.save()

                messages.add_message(
                    request, messages.SUCCESS,
                    "The player %s is dimissed." % membership.player.title)
            else:
                messages.add_message(
                    request, messages.INFO, 'Dismissal canceled.')

            return redirect_to_listing

        context['form'] = form
        return self.render_to_response(context)

    def get(self, request, **kwargs):
        context = self.get_context_data()
        context['form'] = DismissArmyMemberForm()
        return self.render_to_response(context)
