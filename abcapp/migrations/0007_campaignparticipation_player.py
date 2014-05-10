# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abcapp', '0006_campaignparticipation_division'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaignparticipation',
            name='player',
            field=models.ForeignKey(to='abcapp.Player', to_field=u'id'),
            preserve_default=True,
        ),
    ]
