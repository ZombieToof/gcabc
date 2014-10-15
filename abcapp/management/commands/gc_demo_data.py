from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.timezone import utc

from django_phpBB3 import models as phpbb_models

from abcapp import models
from abcapp.tests import factories


class Command(BaseCommand):
    help = 'Add demo data for abcapp'

    @classmethod
    def create_players(cls):
        perm_from_user = phpbb_models.User.objects.first()
        players = []
        for _ in range(200):
            players.append(factories.PlayerFactory(
                phpbb_user__perm_from=perm_from_user))
        return players

    @classmethod
    def create_campaign(cls, title, start, end, army1_name, army1_tag,
                        army2_name, army2_tag, players):

        campaign = factories.CampaignFactory(title=title, start=start,
                                             end=end)
        for (name, tag, army_members) in (
                (army1_name, army1_tag, players[0:len(players)/2]),
                (army2_name, army2_tag, players[(len(players)/2) + 1:])):
            army = factories.FullArmyFactory.create(title=name,
                                                    campaign=campaign)
            army.tag = tag
            divisions = army.divisions.all()
            generals_rank = army.sorted_ranks[0]
            other_ranks = army.sorted_ranks[1:] # all but general
            for index, player in enumerate(army_members):
                division = divisions[index % len(divisions)]
                rank = other_ranks[index % len(other_ranks)]
                models.ArmyMembership.objects.create(player=player,
                                                     army=army,
                                                     rank=rank,
                                                     division=division)
            general = army_members[0]
            army.general = general.phpbb_user
            generals_membership = army.membership_for_player(general)
            generals_membership.rank = generals_rank  # promoted
            print generals_membership.rank

    @classmethod
    def create_campaigns(self, players):
        campaigns = []
        for index, data in enumerate(
            ((u'BF3C6 - UN vs IMF S.C.A.R',
              datetime(2013, 6, 20, tzinfo=utc),
              datetime(2013, 8, 24, tzinfo=utc),
              u'United Nations Security Council', u'UN',
              u'IMF S.C.A.R', u'IMF'),
             (u'BF4C1 - Allied Forces vs. Soviets',
              datetime(2013, 9, 6, tzinfo=utc),
              datetime(2014, 2, 28, tzinfo=utc),
              u'Allied Forces', u'AF',
              u'Soviets', u'SV'),
             (u'BF4C2 - GoCI vs 9th',
              datetime(2014, 3, 29, tzinfo=utc),
              None,
              u'Guild of Calamitous Intent', u'GoCI',
              u'9th Marine Expeditionary Unit', u'9th'))):
            (title, start, end,
             army1_name, army1_tag,
             army2_name, army2_tag) = data
            players_for_campaign = players[(index * 10):(index * 10) + 100]
            campaign = self.create_campaign(title, start, end,
                                            army1_name, army1_tag,
                                            army2_name, army2_tag,
                                            players_for_campaign)
            campaigns.append(campaign)

    def handle(self, **kwargs):
        with transaction.atomic():
            players = self.create_players()
            self.create_campaigns(players)
            self.stdout.write('Created Players and Campaigns')
            self.stdout.write('=============================')

            campaigns = models.Campaign.objects.all()
            self.write_title_list('Campaigns', campaigns)

            for campaign in campaigns:
                self.stdout.write(campaign.title)
                self.stdout.write(len(campaign.title) * '*' + u'\n\n')
                for army in campaign.armies.all():
                    self.stdout.write(army.formated())

            raise ValueError('something might have gone wrong')


    def write_title_list(self, label, items):
        self.stdout.write(label + '\n' + len(label) * '=' + '\n')
        self.stdout.write(u'\n'.join([item.title for item in items]))
        self.stdout.write(u'\n\n')

