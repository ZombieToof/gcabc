from django.contrib import admin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
from django_phpBB3.models import Group as PhpbbGroup
from django_phpBB3.models import Rank as PhpbbRank
from django_phpBB3.models import User as PhpbbUser


class MetadataMixin(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=400)
    description = models.TextField(blank=True)
    creator = models.ForeignKey('auth.User', blank=True, null=True,
                                default=None, editable=False,
                                related_name='+')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            # new object
            self.slug = slugify(self.title)
        super(MetadataMixin, self).save(*args, **kwargs)

    def __str__(self):
        return '<%s %s: %s>' % (self.__class__.__name__, self.id or None,
                                self.title)


class Campaign(MetadataMixin, models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    draft_start = models.DateTimeField(null=True, blank=True)
    draft_end = models.DateTimeField(null=True, blank=True)
    draft_enabled = models.BooleanField(default=False)

    @property
    def details_url(self):
        return reverse('campaign', kwargs={'pk': self.id})

    def battledays(self):
        pass


class Army(MetadataMixin, models.Model):
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


class Division(MetadataMixin, models.Model):
    army = models.ForeignKey(Army)
    logo = models.ImageField(null=True, blank=True)
    commander = models.ForeignKey(PhpbbUser,
                                  related_name='+',  # omit back ref
                                  null=True,
                                  blank=True)
    is_headquater = models.BooleanField(default=False)


class Rank(MetadataMixin, models.Model):
    phpbb_rank = models.OneToOneField(PhpbbRank,
                                      related_name='abc_rank')
    army = models.ForeignKey(Army, related_name='ranks')
    abc_logo = models.ImageField(null=True, blank=True)
    level = models.IntegerField()
    is_officer = models.BooleanField(default=False)


class Medal(MetadataMixin, models.Model):
    army = models.ForeignKey(Army)
    logo = models.ImageField(null=True, blank=True)
    level = models.IntegerField()


class Player(MetadataMixin, models.Model):
    phpbb_user = models.OneToOneField(PhpbbUser,
                                      related_name='player')
    django_user = models.OneToOneField(User,
                                       related_name='player')
    rank = models.ForeignKey(Rank,
                             related_name='players',
                             null=True,
                             blank=True)
    drafted_for = models.ForeignKey(Campaign,
                                    related_name='draftable_players',
                                    null=True,
                                    blank=True)
    medals = models.ManyToManyField(Medal,
                                    related_name='players',
                                    null=True,
                                    blank=True)
    notes = models.TextField(null=True, blank=True)

    def army(self):
        if not self.rank:
            return None
        return self.rank.army


admin.site.register(Campaign)
admin.site.register(Army)
admin.site.register(Rank)
admin.site.register(Medal)
admin.site.register(Player)
