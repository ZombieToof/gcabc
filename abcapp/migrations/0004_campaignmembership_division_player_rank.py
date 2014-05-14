# encoding: utf8
from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('abcapp', '0003_medal'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_phpBB3', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rank',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=400)),
                ('description', models.TextField(blank=True)),
                ('creator', models.ForeignKey(default=None, to_field=u'id', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True, editable=False, blank=True)),
                ('phpbb_rank', models.OneToOneField(to='django_phpBB3.Rank', to_field='id')),
                ('army', models.ForeignKey(to='abcapp.Army', to_field=u'id')),
                ('abc_logo', models.ImageField(null=True, upload_to='', blank=True)),
                ('level', models.IntegerField()),
                ('is_officer', models.BooleanField(default=False)),
            ],
            options={
                u'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CampaignMembership',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('creator', models.ForeignKey(default=None, to_field=u'id', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True, editable=False, blank=True)),
                ('army', models.ForeignKey(to_field=u'id', blank=True, to='abcapp.Army', null=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('campaign', models.ForeignKey(to='abcapp.Campaign', to_field=u'id')),
                ('ranks', models.ManyToManyField(to='abcapp.Rank', null=True, blank=True)),
                ('medals', models.ManyToManyField(to='abcapp.Medal', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=400)),
                ('description', models.TextField(blank=True)),
                ('creator', models.ForeignKey(default=None, to_field=u'id', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True, editable=False, blank=True)),
                ('army', models.ForeignKey(to='abcapp.Army', to_field=u'id')),
                ('logo', models.ImageField(null=True, upload_to='', blank=True)),
                ('is_headquater', models.BooleanField(default=False)),
            ],
            options={
                u'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('creator', models.ForeignKey(default=None, to_field=u'id', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True, editable=False, blank=True)),
                ('django_user', models.OneToOneField(to=settings.AUTH_USER_MODEL, to_field=u'id')),
                ('campaigns', models.ManyToManyField(to='abcapp.Campaign', null=True, through='abcapp.CampaignMembership', blank=True)),
            ],
            options={
                u'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
