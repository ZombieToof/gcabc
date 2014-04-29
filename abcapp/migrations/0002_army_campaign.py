# encoding: utf8
from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('abcapp', '0001_adjust_phpbb'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField()),
                ('title', models.CharField(max_length=400)),
                ('description', models.TextField(blank=True)),
                ('creator', models.ForeignKey(default=None, to_field=u'id', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True, blank=True)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField(null=True, blank=True)),
                ('draft_starts', models.DateTimeField(null=True, blank=True)),
                ('draft_ends', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                u'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Army',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField()),
                ('title', models.CharField(max_length=400)),
                ('description', models.TextField(blank=True)),
                ('creator', models.ForeignKey(default=None, to_field=u'id', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True, blank=True)),
                ('campaign', models.ForeignKey(to='abcapp.Campaign', to_field=u'id')),
                ('logo', models.ImageField(null=True, upload_to='', blank=True)),
                ('tag', models.CharField(max_length=10)),
                ('tag_structure', models.CharField(max_length=200)),
                ('ts_password', models.CharField(max_length=50)),
                ('join_password', models.CharField(max_length=50)),
                ('color', models.CharField(max_length=7)),
                ('draft_enabled', models.BooleanField(default=False)),
                ('hc_forum_group', models.ForeignKey(to_field='id', blank=True, to='django_phpBB3.Group', null=True)),
                ('officers_forum_group', models.ForeignKey(to_field='id', blank=True, to='django_phpBB3.Group', null=True)),
                ('soldiers_forum_group', models.ForeignKey(to_field='id', blank=True, to='django_phpBB3.Group', null=True)),
            ],
            options={
                u'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
