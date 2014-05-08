# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abcapp', '0010_campaignparticipation_division'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rank',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='player',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='medal',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='army',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='campaignparticipation',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='player',
            name='title',
        ),
        migrations.RemoveField(
            model_name='campaignparticipation',
            name='description',
        ),
        migrations.RemoveField(
            model_name='division',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='player',
            name='description',
        ),
        migrations.RemoveField(
            model_name='campaignparticipation',
            name='title',
        ),
        migrations.AlterUniqueTogether(
            name='campaignparticipation',
            unique_together=set([('player', 'campaign')]),
        ),
    ]
