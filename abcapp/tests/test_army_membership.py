from django.core.exceptions import ValidationError
from django.test import TestCase
from abcapp import models
from abcapp.tests.factories import FullArmyFactory
from abcapp.tests.factories import PlayerFactory


class ArmyMembershopTestCase(TestCase):

    def test_rank_army_validation(self):
        '''The membership's army has to match the membership rank's army'''
        army = FullArmyFactory.create(title=u'Test Army')
        other_army = FullArmyFactory.create(title=u'other Army')

        player = PlayerFactory()
        membership = models.ArmyMembership(player=player,
                                           army=army)
        membership.save()

        self.assertEqual(membership.full_clean(), None)

        membership.rank = other_army.ranks.first()

        self.assertRaises(ValidationError, membership.full_clean)

    def test_medal_army_validation(self):
        '''The membership's army has to match the membership medals's army'''
        army = FullArmyFactory.create(title=u'Test Army')
        other_army = FullArmyFactory.create(title=u'other Army')

        player = PlayerFactory()
        membership = models.ArmyMembership(player=player,
                                           army=army)
        membership.save()

        self.assertEqual(membership.full_clean(), None)

        membership.medals.add(other_army.medals.first())

        self.assertRaises(ValidationError, membership.full_clean)

    def test_division_army_validation(self):
        '''The membership's army has to match the membership division's army'''
        army = FullArmyFactory.create(title=u'Test Army')
        other_army = FullArmyFactory.create(title=u'other Army')

        player = PlayerFactory()
        membership = models.ArmyMembership(player=player,
                                           army=army)
        membership.save()

        self.assertEqual(membership.full_clean(), None)

        membership.division = other_army.divisions.first()

        self.assertRaises(ValidationError, membership.full_clean)


