# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abcapp', '0007_campaignparticipation_player'),
        ('django_phpBB3', '__first__'),
    ]

    operations = [
        migrations.AddField(
            model_name='division',
            name='commander',
            field=models.ForeignKey(to_field='id', blank=True, to='django_phpBB3.User', null=True),
            preserve_default=True,
        ),
    ]
