from django.contrib import admin
from django.db import models
from django.template.defaultfilters import slugify


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
    draft_starts = models.DateTimeField()
    draft_ends = models.DateTimeField()


class Army(MetadataMixin, models.Model):
    campaign = models.ForeignKey(Campaign)
    logo = models.ImageField(null=True, blank=True)
    general = models.IntegerField(null=True, blank=True)  # FIXME: FK to a user
    tag = models.CharField(max_length=10)
    tag_structure = models.CharField(max_length=200)
    ts_password = models.CharField(max_length=50)
    join_password = models.CharField(max_length=50)
    color = models.CharField(max_length=7)
    draft_enabled = models.BooleanField(default=False)
    hc_forum_group = models.IntegerField(null=True, blank=True)  # FIXME: FK
    officers_forum_group = models.IntegerField(null=True,
                                               blank=True)  # FIXME: FK
    soldiers_forum_group = models.IntegerField(null=True,  # FIXME: FK
                                               blank=True)


class Division(MetadataMixin, models.Model):
    army = models.ForeignKey(Army)
    logo = models.ImageField(null=True, blank=True)
    commander = models.IntegerField(null=True, blank=True)  # FIXME: FK
    is_headquater = models.BooleanField()


class Rank(MetadataMixin, models.Model):
    army = models.ForeignKey(Army)
    logo = models.ImageField(null=True, blank=True)
    level = models.IntegerField()
    is_officer = models.BooleanField(default=False)
    phpbb_rank = models.IntegerField(null=True, blank=True)  # FIXME: FK


class Medal(MetadataMixin, models.Model):
    army = models.ForeignKey(Army)
    logo = models.ImageField(null=True, blank=True)
    level = models.IntegerField()


class Player(MetadataMixin, models.Model):
    rank = models.ForeignKey(Rank,
                             related_name='players',
                             blank=True)
    drafted_for = models.ManyToManyField(Campaign,
                                         related_name='draftable_players',
                                         blank=True)
    phpbb_user = models.IntegerField()  # FIXME: Foreign Key/OneToOneField
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
