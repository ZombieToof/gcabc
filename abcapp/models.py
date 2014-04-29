from django.contrib import admin
from django.db import models
from django.template.defaultfilters import slugify
from django_phpBB3 import models as phpbb_models


class MetadataMixin(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=400)
    description = models.TextField(blank=True)
    creator = models.ForeignKey('auth.User', blank=True, null=True,
                                default=None, editable=False)
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
    draft_starts = models.DateTimeField(null=True, blank=True)
    draft_ends = models.DateTimeField(null=True, blank=True)


class Army(MetadataMixin, models.Model):
    campaign = models.ForeignKey(Campaign)
    logo = models.ImageField(null=True, blank=True)
    general = models.ForeignKey(phpbb_models.User,
                                related_name='+',  # omit back ref
                                null=True,
                                blank=True)
    tag = models.CharField(max_length=10)
    tag_structure = models.CharField(max_length=200)
    ts_password = models.CharField(max_length=50)
    join_password = models.CharField(max_length=50)
    color = models.CharField(max_length=7)
    draft_enabled = models.BooleanField(default=False)
    hc_forum_group = models.ForeignKey(phpbb_models.Group,
                                       related_name='+',  # omit back ref
                                       null=True,
                                       blank=True)
    officers_forum_group = models.ForeignKey(phpbb_models.Group,
                                             related_name='+',  # omit back ref
                                             null=True,
                                             blank=True)
    soldiers_forum_group = models.ForeignKey(phpbb_models.Group,
                                             related_name='+',  # omit back ref
                                             null=True,
                                             blank=True)


class Division(MetadataMixin, models.Model):
    army = models.ForeignKey(Army)
    logo = models.ImageField(null=True, blank=True)
    commander = models.ForeignKey(phpbb_models.User,
                                  related_name='+',  # omit back ref
                                  null=True,
                                  blank=True)
    is_headquater = models.BooleanField(default=False)


class Rank(MetadataMixin, models.Model):
    phpbb_rank = models.OneToOneField(phpbb_models.Rank,
                                      related_name='abc_rank')
    army = models.ForeignKey(Army)
    abc_logo = models.ImageField(null=True, blank=True)
    level = models.IntegerField()
    is_officer = models.BooleanField(default=False)


class Medal(MetadataMixin, models.Model):
    army = models.ForeignKey(Army)
    logo = models.ImageField(null=True, blank=True)
    level = models.IntegerField()


class Player(MetadataMixin, models.Model):
    phpbb_user = models.ForeignKey(phpbb_models.User,
                                   related_name='soldiers')
    rank = models.ForeignKey(Rank,
                             related_name='players',
                             blank=True)
    drafted_for = models.ManyToManyField(Campaign,
                                         related_name='draftable_players',
                                         blank=True)
    medals = models.ManyToManyField(Medal,
                                    related_name='players',
                                    blank=True)
    notes = models.TextField()

    def army(self):
        if not self.rank:
            return None
        return self.rank.army


admin.site.register(Campaign)
admin.site.register(Army)
admin.site.register(Rank)
admin.site.register(Medal)
admin.site.register(Player)
