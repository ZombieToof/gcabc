from datetime import timedelta
from django.utils import timezone
from factory import DjangoModelFactory
import factory

from abcapp import models


def gen_color(n):
    modulo = n % 3
    color_values = {}
    colors = ['red', 'green', 'blue']
    for index in range(3):
        color_name = colors[index]
        color_value = n * 99
        if index == modulo:
            color_value += n * 12
        color_value = color_value % 255  # reduce to max range
        color_values[color_name] = color_value
    return '#%02X%02X%02X' % (color_values['red'], color_values['green'],
                              color_values['blue'])


def now_plus_days(n, days, days_to_add=0):
    return timezone.now() + timedelta(days=((n*days) + days_to_add))


class CampaignFactory(DjangoModelFactory):

    class Meta:
        model = models.Campaign

    title = factory.Sequence(lambda n: 'BF4C%d' % n)
    start = factory.Sequence(lambda n: now_plus_days(n, 100))
    end = factory.Sequence(lambda n: now_plus_days(n, 100, days_to_add=99))


class DivisionFactory(DjangoModelFactory):

    title = factory.Iterator(['Headquater', 'Airforce', 'Armor', 'Infantrie'])


class RankFactory(DjangoModelFactory):

    title = factory.Iterator(['Private', 'Specialist', 'Major', 'General'])
    level = factory.sequence([1, 10, 20, 40])


class MedalFactory(DjangoModelFactory):

    title = factory.Iterator(['Lead', 'Bronze', 'Silver', 'Gold'])
    level = factory.sequence([1, 10, 20, 40])


class FullArmyFactory(DjangoModelFactory):

    tag = factory.Sequence(lambda n: 'AY%d' % n)
    ts_password = factory.Sequence(lambda n: 'ts_pw%d' % n)
    join_password = factory.Sequence(lambda n: 'join_pw%d' % n)
    ts_password = factory.Sequence(lambda n: 'ts_pw%d' % n)
    color = factory.Sequence(lambda n: gen_color(n))

    # create divisions
    headquater = factory.RelatedFactory(DivisionFactory,
                                        'army', title='Headquater',
                                        id_headquater=True)
    armor = factory.RelatedFactory(DivisionFactory,
                                   'army', title='Armor')
    airforce = factory.RelatedFactory(DivisionFactory,
                                      'army', title='Airforce')
    infantry = factory.RelatedFactory(DivisionFactory,
                                      'army', title='Infantry')

    # create ranks
    private = factory.RelatedFactory(RankFactory,
                                     'army', title='Private', level=1)
    specialist = factory.RelatedFactory(RankFactory,
                                        'army', title='Specialist', level=10)
    major = factory.RelatedFactory(RankFactory,
                                   'army', title='Major', level=20,
                                   is_officer=True)
    general = factory.RelatedFactory(RankFactory,
                                     'army', title='General', level=40,
                                     is_officer=True)

    # create medals
    lead = factory.RelatedFactory(MedalFactory,
                                  'army', title='Lead', level=1)
    Bronze = factory.RelatedFactory(MedalFactory,
                                    'army', title='Bronze', level=10)
    silver = factory.RelatedFactory(MedalFactory,
                                    'army', title='Silver', level=20)
    gold = factory.RelatedFactory(MedalFactory,
                                  'army', title='Gold', level=40)
