from django.test import TestCase
from abcapp import models
from abcapp.tests.factories import FullArmyFactory
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

