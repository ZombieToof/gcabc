from datetime import timedelta
from django.contrib.auth import models as contrib_auth_models
from django.utils import timezone
from django_phpBB3 import models as phpbb_models
from factory import DjangoModelFactory

import factory
import os.path

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


def now_plus_days(number, days, days_to_add=0):
    return timezone.now() + timedelta(days=((number*days) + days_to_add))


def read_data_file(name):
    module_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(module_dir, 'data', name)
    return open(file_path, 'r')


def _names():
    names = []
    names_file = read_data_file('names.csv')
    return [name.strip() for name in names_file]


names = _names()

def make_username(i):
    return '%s(%s)' % (names[i], i)


class PhpbbGroupFactory(DjangoModelFactory):

    class Meta:
        model = phpbb_models.Group

    id = factory.Sequence(lambda n: int(n))
    # required. We don't care in tests, so we assign some values
    skip_auth = 0
    desc = factory.Sequence(lambda n: 'PhpbbGroup%s' % n)
    desc_bitfield = '1'
    desc_uid = factory.Sequence(lambda n: 'Desc%s' % n)
    max_recipients = '1000'


class PhpbbStyleFactory(DjangoModelFactory):
    '''The style of the board, requried by User'''

    class Meta:
        model = phpbb_models.Style

    id = factory.Sequence(lambda n: int(n))
    style_name = factory.Sequence(lambda n: 'Some style %s' % n)
    style_copyright = 'Copyright'


class PhpbbRankFactory(DjangoModelFactory):

    class Meta:
        model = phpbb_models.Rank

    id = factory.Sequence(lambda n: int(n))
    rank_title = factory.Sequence(lambda n: 'PhpbbRank %s' % n)
    rank_image = 'what for'


class PhpbbUserFactory(DjangoModelFactory):

    class Meta:
        model = phpbb_models.User

    id = factory.Sequence(lambda n: int(n))
    username = factory.Sequence(make_username)
    username_clean = factory.Sequence(lambda i: make_username(i).lower())
    email = factory.Sequence(lambda n: 'phpbbuser%s@example.com' % n)
    group = factory.SubFactory(PhpbbGroupFactory)
    style = factory.SubFactory(PhpbbStyleFactory)
    rank = factory.SubFactory(PhpbbRankFactory)
    # required. We don't care in tests, so we assign some values
    new = 1
    reminded = 1
    reminded_time = 1


class DjangoUserFactory(DjangoModelFactory):

    class Meta:
        model = contrib_auth_models.User

    username = factory.Sequence(make_username)


class PlayerFactory(DjangoModelFactory):

    class Meta:
        model = models.Player

    phpbb_user = factory.SubFactory(PhpbbUserFactory)
    django_user = factory.SubFactory(DjangoUserFactory)


class CampaignFactory(DjangoModelFactory):

    class Meta:
        model = models.Campaign

    title = factory.Sequence(lambda n: 'BF4C%d' % n)
    start = factory.Sequence(lambda n: now_plus_days(n, 100))
    end = factory.Sequence(lambda n: now_plus_days(n, 100, days_to_add=99))


class DivisionFactory(DjangoModelFactory):

    class Meta:
        model = models.Division

    title = factory.Iterator(['Headquater', 'Airforce', 'Armor', 'Infantrie'])


class RankFactory(DjangoModelFactory):

    class Meta:
        model = models.Rank

    phpbb_rank = factory.SubFactory(PhpbbRankFactory)
    title = factory.Iterator(['Private', 'Specialist', 'Major', 'General'])
    level = factory.sequence([1, 10, 20, 40])


class MedalFactory(DjangoModelFactory):

    class Meta:
        model = models.Medal

    title = factory.Iterator(['Lead', 'Bronze', 'Silver', 'Gold'])
    level = factory.sequence([1, 10, 20, 40])


class FullArmyFactory(DjangoModelFactory):

    class Meta:
        model = models.Army

    title = factory.Sequence(lambda n: 'Army %s' % n)
    campaign = factory.SubFactory(CampaignFactory)
    tag = factory.Sequence(lambda n: 'AY%d' % n)
    ts_password = factory.Sequence(lambda n: 'ts_pw%d' % n)
    join_password = factory.Sequence(lambda n: 'join_pw%d' % n)
    ts_password = factory.Sequence(lambda n: 'ts_pw%d' % n)
    color = factory.Sequence(lambda n: gen_color(n))

    # create divisions
    headquater = factory.RelatedFactory(DivisionFactory,
                                        'army', title='Headquater',
                                        is_headquater=True)
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
    bronze = factory.RelatedFactory(MedalFactory,
                                    'army', title='Bronze', level=10)
    silver = factory.RelatedFactory(MedalFactory,
                                    'army', title='Silver', level=20)
    gold = factory.RelatedFactory(MedalFactory,
                                  'army', title='Gold', level=40)


class ArmyMembershipFactory(DjangoModelFactory):

    class Meta:
        model = models.ArmyMembership

