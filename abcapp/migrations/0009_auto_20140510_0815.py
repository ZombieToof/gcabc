# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_phpBB3', '__first__'),
        ('abcapp', '0008_division_commander'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='phpbb_user',
            field=models.OneToOneField(to='django_phpBB3.User', to_field='id'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='campaignparticipation',
            unique_together=set([('player', 'campaign')]),
        ),
    ]
