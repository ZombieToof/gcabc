# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abcapp', '0005_army_general'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaignmembership',
            name='division',
            field=models.ForeignKey(to_field=u'id', blank=True, to='abcapp.Division', null=True),
            preserve_default=True,
        ),
    ]
