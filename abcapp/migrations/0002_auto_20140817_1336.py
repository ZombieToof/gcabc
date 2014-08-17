# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_phpBB3', '__first__'),
        ('abcapp', '0001_adjust_phpbb'),
    ]

    operations = [
        migrations.CreateModel(
            name='Army',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=400)),
                ('description', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True, editable=False, blank=True)),
                ('logo', models.ImageField(null=True, upload_to=b'', blank=True)),
                ('tag', models.CharField(max_length=10, null=True, blank=True)),
                ('tag_structure', models.CharField(max_length=200, null=True, blank=True)),
                ('ts_password', models.CharField(max_length=50, null=True, blank=True)),
                ('join_password', models.CharField(max_length=50, null=True, blank=True)),
                ('color', models.CharField(max_length=7)),
                ('creator', models.ForeignKey(related_name=b'+', default=None, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('general', models.ForeignKey(related_name=b'+', blank=True, to='django_phpBB3.User', null=True)),
                ('hc_forum_group', models.ForeignKey(related_name=b'+', blank=True, to='django_phpBB3.Group', null=True)),
                ('officers_forum_group', models.ForeignKey(related_name=b'+', blank=True, to='django_phpBB3.Group', null=True)),
                ('soldiers_forum_group', models.ForeignKey(related_name=b'+', blank=True, to='django_phpBB3.Group', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArmyMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True, editable=False, blank=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('army', models.ForeignKey(to='abcapp.Army')),
                ('creator', models.ForeignKey(related_name=b'+', default=None, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BattleDay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=400)),
                ('description', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True, editable=False, blank=True)),
                ('creator', models.ForeignKey(related_name=b'+', default=None, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BattleDaySignup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True, editable=False, blank=True)),
                ('battleday', models.ForeignKey(related_name=b'signups', to='abcapp.BattleDay')),
                ('creator', models.ForeignKey(related_name=b'+', default=None, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BattleDaySignupQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=400)),
                ('description', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True, editable=False, blank=True)),
                ('creator', models.ForeignKey(related_name=b'+', default=None, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='battleday',
            name='question',
            field=models.ForeignKey(related_name=b'battledays', to='abcapp.BattleDaySignupQuestion'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='BattleDaySignupQuestionChoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=400)),
                ('description', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True, editable=False, blank=True)),
                ('order', models.IntegerField()),
                ('creator', models.ForeignKey(related_name=b'+', default=None, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('question', models.ForeignKey(related_name=b'choices', to='abcapp.BattleDaySignupQuestion')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='battledaysignup',
            name='selected_choices',
            field=models.ManyToManyField(to='abcapp.BattleDaySignupQuestionChoice', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='battledaysignupquestionchoice',
            unique_together=set([('order', 'question')]),
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=400)),
                ('description', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True, editable=False, blank=True)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField(null=True, blank=True)),
                ('draft_start', models.DateTimeField(null=True, blank=True)),
                ('draft_disabled', models.BooleanField(default=False)),
                ('creator', models.ForeignKey(related_name=b'+', default=None, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='battleday',
            name='campaign',
            field=models.ForeignKey(related_name=b'battledays', to='abcapp.Campaign'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='army',
            name='campaign',
            field=models.ForeignKey(related_name=b'armies', to='abcapp.Campaign'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='CampaignMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True, editable=False, blank=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('campaign', models.ForeignKey(related_name=b'memberships', to='abcapp.Campaign')),
                ('creator', models.ForeignKey(related_name=b'+', default=None, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=400)),
                ('description', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True, editable=False, blank=True)),
                ('logo', models.ImageField(null=True, upload_to=b'', blank=True)),
                ('is_headquater', models.BooleanField(default=False)),
                ('army', models.ForeignKey(related_name=b'divisions', to='abcapp.Army')),
                ('commander', models.ForeignKey(related_name=b'+', blank=True, to='django_phpBB3.User', null=True)),
                ('creator', models.ForeignKey(related_name=b'+', default=None, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='armymembership',
            name='division',
            field=models.ForeignKey(related_name=b'memberships', blank=True, to='abcapp.Division', null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Medal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=400)),
                ('description', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True, editable=False, blank=True)),
                ('logo', models.ImageField(null=True, upload_to=b'', blank=True)),
                ('level', models.IntegerField()),
                ('army', models.ForeignKey(related_name=b'medals', to='abcapp.Army')),
                ('creator', models.ForeignKey(related_name=b'+', default=None, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='armymembership',
            name='medals',
            field=models.ManyToManyField(related_name=b'memberships', null=True, to='abcapp.Medal', blank=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True, editable=False, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='campaignmembership',
            name='player',
            field=models.ForeignKey(related_name=b'memberships', to='abcapp.Player'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='campaignmembership',
            unique_together=set([('player', 'campaign')]),
        ),
        migrations.AddField(
            model_name='battledaysignup',
            name='player',
            field=models.ForeignKey(related_name=b'signups', to='abcapp.Player'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='battledaysignup',
            unique_together=set([('battleday', 'player')]),
        ),
        migrations.AddField(
            model_name='armymembership',
            name='player',
            field=models.ForeignKey(to='abcapp.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='armies',
            field=models.ManyToManyField(related_name=b'players', null=True, through='abcapp.ArmyMembership', to='abcapp.Army', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='campaigns',
            field=models.ManyToManyField(related_name=b'players', null=True, through='abcapp.CampaignMembership', to='abcapp.Campaign', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='creator',
            field=models.ForeignKey(related_name=b'+', default=None, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='django_user',
            field=models.OneToOneField(related_name=b'player', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='phpbb_user',
            field=models.OneToOneField(related_name=b'player', to='django_phpBB3.User'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=400)),
                ('description', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True, editable=False, blank=True)),
                ('abc_logo', models.ImageField(null=True, upload_to=b'', blank=True)),
                ('level', models.IntegerField()),
                ('is_officer', models.BooleanField(default=False)),
                ('army', models.ForeignKey(related_name=b'ranks', to='abcapp.Army')),
                ('creator', models.ForeignKey(related_name=b'+', default=None, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('phpbb_rank', models.OneToOneField(related_name=b'abc_rank', to='django_phpBB3.Rank')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='armymembership',
            name='rank',
            field=models.ForeignKey(related_name=b'memberships', blank=True, to='abcapp.Rank', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='armymembership',
            unique_together=set([('player', 'army', 'deleted')]),
        ),
    ]
