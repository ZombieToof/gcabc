# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abcapp', '0009_remove_army_draft_enabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='draft_enabled',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='drafted_for',
            field=models.ForeignKey(to_field=u'id', blank=True, to='abcapp.Campaign', null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='phpbb_user',
            field=models.OneToOneField(to='django_phpBB3.User', to_field='id'),
        ),
    ]
