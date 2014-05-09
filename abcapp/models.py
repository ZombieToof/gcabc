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


class TitleDescriptionMixin(models.Model):

    title = models.CharField(max_length=400)
    description = models.TextField(blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class MetadataMixin(models.Model):
    creator = models.ForeignKey('auth.User', blank=True, null=True,
                                default=None, editable=False,
                                related_name='+')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            # new object
            self.slug = slugify(self.title)
        super(MetadataMixin, self).save(*args, **kwargs)

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

    def participation_for_player(self, player):
        return CampaignParticipation.objects.filter(
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
        self.start and (self.start <= now)

    @property
    def running(self):
        return self.started and not self.finished

    def player_info(self, player):
        participation = self.participation_for_player(player)
        army = participation.army if participation else None
        rank = participation.rank if participation else None
        medals = participation.medals if participation else []
        division = participation.division if participation else None
        has_joined = bool(participation)

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

    def sorted_ranks(self):
        return self.ranks.order_by('-level', 'title')


class Division(TitleDescriptionMixin, MetadataMixin, models.Model):
    army = models.ForeignKey(Army)
    logo = models.ImageField(null=True, blank=True)
    commander = models.ForeignKey(PhpbbUser,
                                  related_name='+',  # omit back ref
                                  null=True,
                                  blank=True)
    is_headquater = models.BooleanField(default=False)


class Rank(TitleDescriptionMixin, MetadataMixin, models.Model):
    phpbb_rank = models.OneToOneField(PhpbbRank,
                                      related_name='abc_rank')
    army = models.ForeignKey(Army, related_name='ranks')
    abc_logo = models.ImageField(null=True, blank=True)
    level = models.IntegerField()
    is_officer = models.BooleanField(default=False)


class Medal(TitleDescriptionMixin, MetadataMixin, models.Model):
    army = models.ForeignKey(Army)
    logo = models.ImageField(null=True, blank=True)
    level = models.IntegerField()


class CampaignParticipation(MetadataMixin, models.Model):

    ranks = models.ManyToManyField(Rank,
                                   related_name='players',
                                   null=True,
                                   blank=True)
    army = models.ForeignKey(Army,
                             related_name='players',
                             null=True,
                             blank=True)
    division = models.ForeignKey(Division,
                                 related_name='players',
                                 null=True,
                                 blank=True)
    medals = models.ManyToManyField(Medal,
                                    related_name='players',
                                    null=True,
                                    blank=True)
    notes = models.TextField(null=True, blank=True)

    player = models.ForeignKey('Player',
                               related_name='participations')

    campaign = models.ForeignKey(Campaign,
                                 related_name='participations')

    class Meta(object):
        unique_together = (('player', 'campaign'),)

    def rank(self):
        return self.ranks.filter(army=self.army)

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
                                       through=CampaignParticipation,
                                       null=True,
                                       blank=True)

    @property
    def title(self):
        return self.phpbb_user.username

    def cached_army_info(self):
        cache = get_request_cache()
        if not 'player_to_army_info' in cache:
            print 'calc info'
            running_campaign = Campaign.current_campaigns().first()
            armies = running_campaign.armies.all()
            player_to_army_info = {}
            for army in armies:
                color = army.color
                players = army.players.all()
                for player in players:
                    player_to_army_info[player.id] = {'color': color,
                                                      'title': army.title}

            cache.set('player_to_army_info', player_to_army_info)

        return cache.get('player_to_army_info').get(self.id)

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
