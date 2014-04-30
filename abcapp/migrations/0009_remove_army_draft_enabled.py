# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abcapp', '0008_auto_20140430_0902'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='army',
            name='draft_enabled',
        ),
    ]
