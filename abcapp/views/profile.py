# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView
from django.template import defaultfilters
from django.utils import timezone

from abcapp.models import Campaign


def format_date(date):
    return defaultfilters.date(date, arg="DATETIME_FORMAT")


class ProfileView(TemplateView):

    template_name = 'profile/index.html'

    def add_status_table_data(self, campaign, info):
        now = timezone.now()
        data = []

        def add(title, value):
            data.append({'title': title,
                         'value': value})

        # status
        status = info['status']
        if campaign.in_join_phase and campaign.draft_disabled:
            status = u"%s (Draft on hold)" % status
        add(u'Status', status)

        if campaign.draft_start and campaign.draft_start > now:
            add(u'Draft start', campaign.draft_start)

        if campaign.running:
            add(u'Campaign started', format_date(campaign.start))

        if campaign.finished:
            dates = [format_date(campaign.start), format_date(campaign.end)]
            date_string = u' – '.join(dates)
            add(u'Campingn start/end', date_string)

        info['status_table_data'] = data

    def campaign_infos(self, player, campaigns):
        infos = []
        for campaign in campaigns:
            info = campaign.player_info(player)
            self.add_status_table_data(campaign, info)
            infos.append(info)
        return infos

    def get_context_data(self, **context):
        user = getattr(self.request, 'user', None)
        context['user'] = user
        if not user:
            context['no_user'] = True
            return context
        try:
            player = user.player
        except (AttributeError, ObjectDoesNotExist):
            context['no_player'] = True
            return context
        if user.is_anonymous():
            context['is_anonymous'] = True
            return context

        current = Campaign.current_campaigns()
        past = Campaign.past_campaigns()
        upcoming = Campaign.upcoming_campaigns()
        context['campaign_lists'] = [
            {'campaigns': self.campaign_infos(player, current),
             'title': u'Current Campaign'},
            {'campaigns': self.campaign_infos(player, upcoming),
             'title': u'Upcoming Campaigns'},
            {'campaigns': self.campaign_infos(player, past),
             'title': u'Past Campaigns'}]

        return context
