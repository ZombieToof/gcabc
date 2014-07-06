# encoding: utf8
from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('abcapp', '0012_battledaysignupquestionchoice'),
    ]

    operations = [
        migrations.CreateModel(
            name='BattleDaySignup',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('creator', models.ForeignKey(default=None, to_field=u'id', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True, editable=False, blank=True)),
                ('battleday', models.ForeignKey(to='abcapp.BattleDay', to_field=u'id')),
                ('player', models.ForeignKey(to='abcapp.Player', to_field=u'id')),
                ('selected_choices', models.ManyToManyField(to='abcapp.BattleDaySignupQuestionChoice', null=True, blank=True)),
            ],
            options={
                u'unique_together': set([('battleday', 'player')]),
            },
            bases=(models.Model,),
        ),
    ]
