from django.contrib.auth import models as auth_models
from django.test import TestCase
from django_phpBB3 import models as phpbb_models
from abcapp import models
from abcapp.tests.factories import ArmyMembershipFactory
from abcapp.tests.factories import CampaignFactory
from abcapp.tests.factories import DjangoUserFactory
from abcapp.tests.factories import FullArmyFactory
from abcapp.tests.factories import PhpbbUserFactory
from abcapp.tests.factories import PlayerFactory


class PlayerTestCase(TestCase):

    def test_player_factories(self):
        phpbb_user = PhpbbUserFactory.create()
        self.assertEqual(phpbb_models.User.objects.first().username,
                         phpbb_user.username)
        django_user = DjangoUserFactory.create()
        self.assertEqual(auth_models.User.objects.first().username,
                         django_user.username)

        # If we call the player factory, it will create new phpbb and
        # django users
        PlayerFactory.create()
        self.assertEqual(len(models.Player.objects.all()), 1)
        self.assertEqual(len(phpbb_models.User.objects.all()), 2)
        self.assertEqual(len(auth_models.User.objects.all()), 2)

        # If we call the player factory and pass the users, it won't
        # create new ones
        PlayerFactory.create(phpbb_user=phpbb_user, django_user=django_user)
        self.assertEqual(len(models.Player.objects.all()), 2)
        self.assertEqual(len(phpbb_models.User.objects.all()), 2)
        self.assertEqual(len(auth_models.User.objects.all()), 2)

    def test_database_is_reset_for_each_test(self):
        # just for the lolz
        PhpbbUserFactory.create()
        self.assertEqual(len(phpbb_models.User.objects.all()), 1)

    def test_player_as_army_member(self):
        army = FullArmyFactory.create(title=u'Test Army')
        player = PlayerFactory.create()

        # make the player a member of the army
        models.ArmyMembership.objects.create(player=player, army=army)
        self.assertEqual(len(models.ArmyMembership.objects.all()), 1)
        self.assertEqual(len(player.armies.all()), 1)
        self.assertEqual(player.armies.first().title, u'Test Army')

    def test_player_can_join_campaign(self):
        campaign = CampaignFactory.create(title=u'Test Campaign')
        player = PlayerFactory.create()

        # make the player join a campaign
        models.CampaignMembership.objects.create(campaign=campaign,
                                                 player=player)
        self.assertEqual(len(models.CampaignMembership.objects.all()), 1)
        self.assertEqual(len(player.campaigns.all()), 1)
        self.assertEqual(player.campaigns.first().title, u'Test Campaign')
