from django.contrib.auth import models as auth_models
from django.test import TestCase
from django_phpBB3 import models as phpbb_models
from abcapp import models
from abcapp.tests.factories import CampaignFactory
from abcapp.tests.factories import DjangoUserFactory
from abcapp.tests.factories import FullArmyFactory
from abcapp.tests.factories import PhpbbUserFactory
from abcapp.tests.factories import PlayerFactory


class DivisionTestCase(TestCase):

    def test_division_playes(self):
        army = FullArmyFactory.create(title=u'Test Army')
        self.assertEqual(army.players.count(), 0)

        player = PlayerFactory()
        membership = models.ArmyMembership(player=player,
                                           army=army)
        membership.save()
        self.assertTrue(player in army.players.all())

