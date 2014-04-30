# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abcapp', '0007_player_phpbb_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='campaign',
            old_name='draft_starts',
            new_name='draft_start',
        ),
        migrations.RenameField(
            model_name='campaign',
            old_name='draft_ends',
            new_name='draft_end',
        ),
    ]
