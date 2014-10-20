from django.test import TestCase
from abcapp import models
from abcapp.tests.factories import FullArmyFactory
from abcapp.tests.factories import PlayerFactory


class DivisionTestCase(TestCase):

    def test_division_playes(self):
        army = FullArmyFactory.create(title=u'Test Army')
        division = army.divisions.first()
        self.assertEqual(division.players.count(), 0)

        player = PlayerFactory()
        membership = models.ArmyMembership(player=player,
                                           army=army,
                                           division=division)
        membership.save()
        self.assertTrue(player in division.players.all())

