# encoding: utf8
from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('abcapp', '0010_battledaysignupquestion'),
    ]

    operations = [
        migrations.CreateModel(
            name='BattleDay',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=400)),
                ('description', models.TextField(blank=True)),
                ('creator', models.ForeignKey(default=None, to_field=u'id', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True, editable=False, blank=True)),
                ('campaign', models.ForeignKey(to='abcapp.Campaign', to_field=u'id')),
                ('question', models.ForeignKey(to='abcapp.BattleDaySignupQuestion', to_field=u'id')),
            ],
            options={
                u'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
