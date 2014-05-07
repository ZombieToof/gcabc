# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abcapp', '0009_auto_20140507_1929'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaignparticipation',
            name='division',
            field=models.ForeignKey(to_field=u'id', blank=True, to='abcapp.Division', null=True),
            preserve_default=True,
        ),
    ]