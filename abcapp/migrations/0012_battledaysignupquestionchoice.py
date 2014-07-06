# encoding: utf8
from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('abcapp', '0011_battleday'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BattleDaySignupQuestionChoice',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=400)),
                ('description', models.TextField(blank=True)),
                ('creator', models.ForeignKey(default=None, to_field=u'id', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True, editable=False, blank=True)),
                ('order', models.IntegerField()),
                ('question', models.ForeignKey(to='abcapp.BattleDaySignupQuestion', to_field=u'id')),
            ],
            options={
                u'unique_together': set([('order', 'question')]),
            },
            bases=(models.Model,),
        ),
    ]
