from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.html import format_html
from django_phpBB3.models import Group as PhpbbGroup
from django_phpBB3.models import Rank as PhpbbRank
from django_phpBB3.models import User as PhpbbUser


from abcapp.middleware.cache import get_request_cache


class SoftDeleteManager(models.Manager):
    ''' Use this manager to get objects that have a deleted field '''
    def get_queryset(self):
        qs = super(SoftDeleteManager, self).get_queryset()
        return qs.filter(deleted__isnull=True)

    @property
    def with_deleted_set(self):
        return super(SoftDeleteManager, self).get_queryset()

    @property
    def deleted_set(self):
        qs = super(SoftDeleteManager, self).get_queryset()
        return qs.filter(deleted__isnull=False)


class TitleDescriptionMixin(models.Model):

    title = models.CharField(max_length=400)
    description = models.TextField(blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            # new object
            self.slug = slugify(self.title)
        super(MetadataMixin, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class MetadataMixin(models.Model):
    creator = models.ForeignKey('auth.User', blank=True, null=True,
                                default=None, editable=False,
                                related_name='+')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True, editable=False)

    objects = SoftDeleteManager()

    class Meta:
        abstract = True

    def delete(self):
        self.deleted = timezone.now()

    def __str__(self):
        return self.title


class Campaign(TitleDescriptionMixin, MetadataMixin, models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    draft_start = models.DateTimeField(null=True, blank=True)
    draft_disabled = models.BooleanField(default=False)

    @property
    def details_url(self):
        return reverse('campaign', kwargs={'pk': self.id})

    def battledays(self):
        pass

    @classmethod
    def current_campaigns(cls):
        q_start = Q(start__lt=timezone.now())
        q_end = (Q(end__gt=timezone.now()) | Q(end=None))
        return cls.objects.filter(q_start & q_end)

    @classmethod
    def upcoming_campaigns(cls):
        q_start = (Q(start__gt=timezone.now()) | Q(start=None))
        return cls.objects.filter(q_start)

    @classmethod
    def past_campaigns(cls):
        q_end = Q(end__lt=timezone.now())
        return cls.objects.filter(q_end)

    def membership_for_player(self, player):
        return CampaignMembership.objects.filter(
            player=player, campaign=self).first()

    def joinable(self):
        # overrule everything
        if self.draft_disabled:
            return False

        if self.in_join_phase:
            return True

        # No dice
        return False

    @property
    def in_join_phase(self):
        # draft or campaign started
        start = self.draft_start or self.start
        now = timezone.now()
        if start and start <= now and not self.finished:
            return True

    @property
    def finished(self):
        now = timezone.now()
        return self.end < now if self.end else False

    @property
    def started(self):
        now = timezone.now()
        return self.start and (self.start <= now)

    @property
    def running(self):
        return self.started and not self.finished

    def player_info(self, player):
        membership = self.membership_for_player(player)
        army = membership.army if membership else None
        rank = membership.rank if membership else None
        medals = membership.medals if membership else []
        division = membership.division if membership else None
        has_joined = bool(membership)

        info = dict(
            has_joined=has_joined,
            can_join=self.joinable() and not has_joined,
            draft_start=self.draft_start,
            draft_disabled=self.draft_disabled,
            start=self.start,
            end=self.end,
            title=self.title,
            description=self.description,
            campaign_armies=self.armies.all(),
            details_url=reverse('abcapp.campaign', args=(self.id,)),
            join_url=reverse('abcapp.campaign.join', args=(self.id,)),
            army=army,
            division=division,
            rank=rank,
            medals=medals,
            status=self.status())

        return info

    def status(self):
        now = timezone.now()
        if self.finished:
            return 'Finished'
        elif self.running:
            return 'Running'
        elif self.joinable():
            return 'In Draft'
        elif self.draft_start and self.draft_start > now:
            return 'Draft upcoming'
        elif self.start and self.start > now:
            return 'Upcoming'
        return 'Unknown'


class Army(TitleDescriptionMixin, MetadataMixin, models.Model):
    campaign = models.ForeignKey(Campaign, related_name="armies")
    logo = models.ImageField(null=True, blank=True)
    general = models.ForeignKey(PhpbbUser,
                                related_name='+',  # omit back ref
                                null=True,
                                blank=True)
    tag = models.CharField(max_length=10, null=True, blank=True)
    tag_structure = models.CharField(max_length=200, null=True, blank=True)
    ts_password = models.CharField(max_length=50, null=True, blank=True)
    join_password = models.CharField(max_length=50, null=True, blank=True)
    color = models.CharField(max_length=7)
    hc_forum_group = models.ForeignKey(PhpbbGroup,
                                       related_name='+',  # omit back ref
                                       null=True,
                                       blank=True)
    officers_forum_group = models.ForeignKey(PhpbbGroup,
                                             related_name='+',  # omit back ref
                                             null=True,
                                             blank=True)
    soldiers_forum_group = models.ForeignKey(PhpbbGroup,
                                             related_name='+',  # omit back ref
                                             null=True,
                                             blank=True)

    @property
    def sorted_ranks(self):
        return self.ranks.order_by('-level', 'title')

    @property
    def sorted_medals(self):
        return self.medals.order_by('-level', 'title')

    def membership_for_player(self, player):
        membership = ArmyMembership.objects.filter(
            army=self, player=player).first()
        return membership

    def is_officer(self, player):
        membership = self.membership_for_player(player)
        rank = membership.rank
        if not rank:
            return False
        return rank.is_officer

    @property
    def details_url(self):
        return reverse('abcapp.campaign.army.details',
                       kwargs={'pk': self.campaign.id,
                               'army_id': self.id})

    def formated(self):

        general = None
        if self.general:
            general = self.general.username
        out = (self.title + '\n' +
               len(self.title) * u'*' + '\n' +
               u'General: %s\n' % general +
               u'Tag: %s\n' % self.tag +
               '\n' +
               '\n')
        for division in self.divisions.all():
            commander = None
            if division.commander:
                commander = division.commander.username

            out = (out +
                   'Division: ' + division.title + '\n' +
                   (10 + len(division.title)) * '-' + '\n' +
                   'Headquater: %s\n' % division.is_headquater +
                   'Commander: %s\n' % commander +
                   'Players:\n')

            for membership in division.memberships.all():
                out = out + u' * %s\n' % membership.player.phpbb_user.username

            out = out + '\n\n'
        return out


class Division(TitleDescriptionMixin, MetadataMixin, models.Model):
    army = models.ForeignKey(Army, related_name='divisions')
    logo = models.ImageField(null=True, blank=True)
    commander = models.ForeignKey(PhpbbUser,
                                  related_name='+',  # omit back ref
                                  null=True,
                                  blank=True)
    is_headquater = models.BooleanField(default=False)

    @property
    def players(self):
        return Player.objects.filter(armymembership__division=self).all()


class Rank(TitleDescriptionMixin, MetadataMixin, models.Model):
    phpbb_rank = models.OneToOneField(PhpbbRank,
                                      related_name='abc_rank')
    army = models.ForeignKey(Army, related_name='ranks')
    abc_logo = models.ImageField(null=True, blank=True)
    level = models.IntegerField()
    is_officer = models.BooleanField(default=False)


class Medal(TitleDescriptionMixin, MetadataMixin, models.Model):
    army = models.ForeignKey(Army, related_name='medals')
    logo = models.ImageField(null=True, blank=True)
    level = models.IntegerField()

    @property
    def players(self):
        # TODO: optimize into one query?
        return [m.player for m in self.memberships]


class ArmyMembership(MetadataMixin, models.Model):

    player = models.ForeignKey('Player')

    army = models.ForeignKey(Army)

    rank = models.ForeignKey(Rank,
                             related_name='memberships',
                             null=True,
                             blank=True)
    division = models.ForeignKey(Division,
                                 related_name='memberships',
                                 null=True,
                                 blank=True)
    medals = models.ManyToManyField(Medal,
                                    related_name='memberships',
                                    null=True,
                                    blank=True)
    notes = models.TextField(null=True, blank=True)

    class Meta(object):
        unique_together = (('player', 'army', 'deleted'),)
        # FIXME: can we test for army.campaign?

    def _assert_army(self, foreign):
        assert foreign.army == self.army, 'Armies do not match: %s != %s' % (
            self.army, foreign.army)

    def set_division(self, division):
        self._assert_army()
        self.division = division

    def set_rank(self, rank):
        self._assert_army()
        # FIXME: if we support demotion we need an ManyToMany field
        self.rank = rank

    def add_medal(self, medal):
        self._assert_army()
        self.medals.add(medal)

    @property
    def title(self):
        army_title = self.army.title if self.army else u'No Army'
        return u'Army: %s(%s) - Player: %s (%s)' % (
            self.army.id, army_title,
            self.player.id, self.player.title)


class CampaignMembership(MetadataMixin, models.Model):
    """Hold signups for campaigns"""

    campaign = models.ForeignKey(Campaign,
                                 related_name='memberships')

    player = models.ForeignKey('Player',
                               related_name='memberships')

    notes = models.TextField(null=True, blank=True)

    class Meta(object):
        unique_together = (('player', 'campaign'),)

    @property
    def army_membership(self):
        return ArmyMembership.objects.filter(
            player=self.player,
            campaign=self.campaign).first()

    @property
    def army(self):
        army_membership = self.army_membership
        if army_membership is None:
            return None
        return self.army_membership.army

    @property
    def title(self):
        return u'%s - %s' % (self.player.title, self.campaign.title)


class Player(MetadataMixin, models.Model):

    phpbb_user = models.OneToOneField(PhpbbUser,
                                      related_name='player')

    django_user = models.OneToOneField(User,
                                       related_name='player')

    campaigns = models.ManyToManyField(Campaign,
                                       related_name='players',
                                       through=CampaignMembership,
                                       null=True,
                                       blank=True)

    armies = models.ManyToManyField(Army,
                                    related_name='players',
                                    through=ArmyMembership,
                                    null=True,
                                    blank=True)

    @property
    def title(self):
        return '%s (phpbb: %s (%s), django: %s (%s))' % (
            self.id, self.phpbb_user.id, self.phpbb_user.username,
            self.django_user.id, self.django_user.username)

    def cached_army_info(self):
        cache = get_request_cache()
        if not 'membership_to_army_info' in cache:
            print 'calc info'
            running_campaign = Campaign.current_campaigns().first()
            armies = running_campaign.armies.all()
            membership_to_army_info = {}
            for army in armies:
                color = army.color
                memberships = army.memberships.all()
                for membership in memberships:
                    membership_to_army_info[membership.id] = {
                        'color': color,
                        'title': army.title}

            cache.set('membership_to_army_info', membership_to_army_info)

        return cache.get('membership_to_army_info').get(self.id)

    def colored_name(self):
        color_style = ''
        army = ''

        info = self.cached_army_info()
        if info:
            color_style = 'color: #%s' % info['color']
            army = '(%s)' % info['title']

        return format_html(
            '&nbsp;&nbsp;<span style="font-size: 12px; '
            'font-weight: bold; {0};">{1} {2}</span>',
            color_style, self.title, army)

    colored_name.allow_tags = True


class BattleDaySignupQuestion(TitleDescriptionMixin, MetadataMixin,
                              models.Model):
    '''A question that can be asked during a battle day signup'''


class BattleDaySignupQuestionChoice(TitleDescriptionMixin, MetadataMixin,
                                    models.Model):

    order = models.IntegerField()
    question = models.ForeignKey(BattleDaySignupQuestion,
                                 related_name='choices')

    class Meta:
        unique_together = (('order', 'question'),)


class BattleDay(TitleDescriptionMixin, MetadataMixin, models.Model):

    campaign = models.ForeignKey(Campaign, related_name='battledays')
    question = models.ForeignKey(BattleDaySignupQuestion,
                                 related_name='battledays')


class BattleDaySignup(MetadataMixin, models.Model):

    battleday = models.ForeignKey(BattleDay, related_name='signups')
    player = models.ForeignKey(Player, related_name='signups')
    selected_choices = models.ManyToManyField(BattleDaySignupQuestionChoice,
                                              null=True,
                                              blank=True)

    class Meta(object):
        unique_together = (('battleday', 'player'),)

