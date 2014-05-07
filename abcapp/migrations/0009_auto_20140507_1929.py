# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abcapp', '0008_player_phpbb_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='draft_disabled',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='draft_end',
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='draft_enabled',
        ),
    ]
